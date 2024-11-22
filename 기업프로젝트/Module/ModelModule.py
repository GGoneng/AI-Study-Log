import os
import torch
import torch.nn as nn
import pickle
import pandas as pd
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, RobustScaler
import torch.optim as optim
import torch.optim.lr_scheduler as lr_scheduler
from torchmetrics.regression import R2Score, MeanAbsoluteError, MeanAbsolutePercentageError, MeanSquaredError

class CustomDataset(Dataset):
    def __init__(self, featureDF, targetDF):
        self.featureDF = featureDF
        self.targetDF = targetDF
        self.n_rows = self.featureDF.shape[0]
        self.n_cols = self.featureDF.shape[1]

    def __len__(self):
        return self.n_rows
    
    def __getitem__(self, index):
        featureTS = torch.FloatTensor(self.featureDF.iloc[index].values)
        targetTS = torch.FloatTensor(self.targetDF.iloc[index].values)

        return featureTS, targetTS       
    

class LSTMModel(nn.Module):
    def __init__(self, hidden_dim, input_size, n_layers, dropout,
                 bidirectional):
        super().__init__()

        self.model = nn.LSTM(
            input_size = input_size,
            hidden_size = hidden_dim,
            num_layers = n_layers,
            dropout = dropout,
            bidirectional = bidirectional,
            batch_first = True
        )

        if bidirectional:
            self.linear = nn.Linear(hidden_dim * 2, 1)
        
        else:
            self.linear = nn.Linear(hidden_dim, 1)

        # 성능에 따라 추가
        # self.dropout = nn.Dropout(dropout)

    def forward(self, inputs):
        output, _ = self.model(inputs)
        logits = self.linear(output)

        return logits


def testing(featureDF, targetDF, model, DEVICE):
    featureTS = torch.FloatTensor(featureDF.values).to(DEVICE)
    targetTS = torch.FloatTensor(targetDF.values).to(DEVICE)
    
    model.eval()
    
    with torch.no_grad():
        pre_val = model(featureTS)
        mae_loss_val = MeanAbsoluteError()(pre_val, targetTS)
        mape_loss_val = MeanAbsolutePercentageError()(pre_val, targetTS)
        mse_loss_val = MeanSquaredError()(pre_val, targetTS)
        score_val = R2Score()(pre_val, targetTS)
    
    return mae_loss_val, mape_loss_val, mse_loss_val, score_val, pre_val


def training(testDF, testtargetDF, model, trainDL,
              optimizer, EPOCH, scheduler, DEVICE):
    SAVE_PATH = './saved_models/'
    os.makedirs(SAVE_PATH, exist_ok = True)

    BREAK_CNT_LOSS = 0
    BREAK_CNT_SCORE = 0
    LIMIT_VALUE = 10

    MAE_LOSS_HISTORY, MAPE_LOSS_HISTORY, MSE_LOSS_HISTORY, SCORE_HISTORY = [[], []], [[], []], [[], []], [[], []]

    for epoch in range(1, EPOCH + 1):
        SAVE_MODEL = os.path.join(SAVE_PATH, f'model_{epoch}.pth')
        SAVE_WEIGHT = os.path.join(SAVE_PATH, f'model_weights_{epoch}.pth')

        mae_loss_total, mape_loss_total, mse_loss_total, score_total = 0, 0, 0, 0

        for featureTS, targetTS in trainDL:
            pre_y = model(featureTS)

            mae_loss = MeanAbsoluteError()(pre_y, targetTS)
            mape_loss = MeanAbsolutePercentageError()(pre_y, targetTS)
            mse_loss = MeanSquaredError()(pre_y, targetTS)

            mae_loss_total += mae_loss.item()
            mape_loss_total += mape_loss.item()
            mse_loss_total += mse_loss.item()

            score = R2Score()(pre_y, targetTS)
            score_total += score.item()

            total_loss = mae_loss + mape_loss + mse_loss

            optimizer.zero_grad()
            
            total_loss.backward()

            optimizer.step()

        test_mae_loss, test_mape_loss, test_mse_loss, test_score, pre_val = testing(testDF, testtargetDF, model, DEVICE)

        MAE_LOSS_HISTORY[1].append(test_mae_loss)
        MAPE_LOSS_HISTORY[1].append(test_mape_loss)
        MSE_LOSS_HISTORY[1].append(test_mse_loss)
        SCORE_HISTORY[1].append(test_score)

        MAE_LOSS_HISTORY[0].append(mae_loss_total / len(trainDL))
        MAPE_LOSS_HISTORY[0].append(mape_loss_total / len(trainDL))
        MSE_LOSS_HISTORY[0].append(mse_loss_total / len(trainDL))
        SCORE_HISTORY[0].append(score_total / len(trainDL))

        print(f'pre_val : {pre_val.squeeze().tolist()[:10]}\ny_val : {testtargetDF.values.squeeze()[:10]}\n')
        print(f'[{epoch} / {EPOCH}]\n- TRAIN MAE LOSS : {MAE_LOSS_HISTORY[0][-1]}')
        print(f'- TRAIN MAPE LOSS : {MAPE_LOSS_HISTORY[0][-1]}')
        print(f'- TRAIN MSE LOSS : {MSE_LOSS_HISTORY[0][-1]}')
        print(f'- TRAIN R2 SCORE : {SCORE_HISTORY[0][-1]}')

        print(f'\n- TEST MAE LOSS : {MAE_LOSS_HISTORY[1][-1]}')
        print(f'- TEST MAPE LOSS : {MAPE_LOSS_HISTORY[1][-1]}')
        print(f'- TEST MSE LOSS : {MSE_LOSS_HISTORY[1][-1]}')
        print(f'- TEST R2 SCORE : {SCORE_HISTORY[1][-1]}')

        scheduler.step(test_mae_loss)

        if len(MAE_LOSS_HISTORY[1]) >= 2:
            if MAE_LOSS_HISTORY[1][-1] >= MAE_LOSS_HISTORY[1][-2]: BREAK_CNT_LOSS += 1
        
        if len(MAE_LOSS_HISTORY[1]) == 1:
            torch.save(model.state_dict(), SAVE_WEIGHT)
            torch.save(model, SAVE_MODEL)

        else:
            if MAE_LOSS_HISTORY[1][-1] < min(MAE_LOSS_HISTORY[1][:-1]):
                torch.save(model.state_dict(), SAVE_WEIGHT)
                torch.save(model, SAVE_MODEL)

        if BREAK_CNT_LOSS > LIMIT_VALUE:
            print(f"성능 및 손실 개선이 없어서 {epoch} EPOCH에 학습 중단")
            # break

    return MAE_LOSS_HISTORY, MAPE_LOSS_HISTORY, MSE_LOSS_HISTORY, SCORE_HISTORY


