import os
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
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
    def __init__(self, featureDF):
        self.featureDF = featureDF
        self.n_rows = self.featureDF.shape[0]
        self.n_cols = self.featureDF.shape[1]

    def __len__(self):
        return self.n_rows
    
    def __getitem__(self, index):
        featureTS = torch.FloatTensor(self.featureDF.iloc[index].values)

        return featureTS, featureTS       
    

class LSTMAutoEncoderModel(nn.Module):
    def __init__(self, input_size, latent_dim, n_layers):
        super().__init__()

        self.encoder = nn.GRU(
            input_size = input_size,
            hidden_size = latent_dim,
            num_layers = n_layers,
            batch_first = True
        )

        # self.latent_layer = nn.Linear(hidden_dim, latent_dim)

        self.decoder = nn.GRU(
            input_size = latent_dim,
            hidden_size = input_size,
            num_layers = n_layers,
            batch_first = True
        )

        self.output_layer = nn.Linear(input_size, input_size)

    def forward(self, inputs):
        inputs = inputs.unsqueeze(1)

        _, encoder = self.encoder(inputs)

        if self.encoder.bidirectional:
            encoder = torch.cat([encoder[-2], encoder[-1]], dim = -1)
        else:
            encoder = encoder[-1]

        decoder, _ = self.decoder(encoder)

        reconstruction = self.output_layer(decoder.squeeze(1))

        return reconstruction
    

def testing(featureDF, targetDF, model, DEVICE):
    featureTS = torch.FloatTensor(featureDF.values).to(DEVICE)
    targetTS = torch.FloatTensor(targetDF.values).to(DEVICE)
    
    model.eval()
    
    with torch.no_grad():
        decoder = model(featureTS)
        loss_val = MeanAbsoluteError()(decoder, targetTS)

    return loss_val

def training(model, trainDL, optimizer, penalty, threshold,
             EPOCH, scheduler, DEVICE):
    
    SAVE_PATH = './saved_models/'
    os.makedirs(SAVE_PATH, exist_ok = True)

    BREAK_CNT_LOSS = 0
    BREAK_CNT_SCORE = 0

    LOSS_HISTORY = []

    for epoch in range(1, EPOCH + 1):
        model.train()
        SAVE_MODEL = os.path.join(SAVE_PATH, f'model_{epoch}.pth')
        SAVE_WEIGHT = os.path.join(SAVE_PATH, f'model_weights_{epoch}.pth')

        loss_total = 0

        for featureTS, targetTS in trainDL:
            featureTS = featureTS.to(DEVICE)
            targetTS = targetTS.to(DEVICE)

            # Forward pass
            reconstructed = model(featureTS)
            loss = CustomPenaltyLoss(penalty, threshold)(reconstructed, targetTS)
            
            loss_total += loss.item()
           
            optimizer.zero_grad()
        
            loss.backward()
        
            optimizer.step()


        LOSS_HISTORY.append(loss_total / len(trainDL))
        train_vae_loss = (loss_total / len(trainDL))
        print(f'[{epoch} / {EPOCH}]\n- TRAIN LOSS : {LOSS_HISTORY[-1]}')

        print(targetTS[0])
        print(reconstructed[0])
        scheduler.step(train_vae_loss)

        if len(LOSS_HISTORY) >= 2:
            if LOSS_HISTORY[-1] >= LOSS_HISTORY[-2]: BREAK_CNT_LOSS += 1
        
        if len(LOSS_HISTORY) == 1:
            torch.save(model.state_dict(), SAVE_WEIGHT)
            torch.save(model, SAVE_MODEL)

        else:
            if LOSS_HISTORY[-1] < min(LOSS_HISTORY[:-1]):
                torch.save(model.state_dict(), SAVE_WEIGHT)
                torch.save(model, SAVE_MODEL)


    return LOSS_HISTORY

class CustomPenaltyLoss(nn.Module):
    def __init__(self, penalty_weight, threshold):
        super().__init__()
        self.penalty_weight = penalty_weight
        self.threshold = threshold
        self.mse_loss = nn.MSELoss()

    def forward(self, original, reconstructed):
        reconstructed_loss = self.mse_loss(reconstructed, original)

        original_diff = original[:, 1:] - original[:, :-1]
        reconstructed_diff = reconstructed[:, 1:] - reconstructed[:, :-1]

        original_diff_abs = torch.abs(original_diff)
        penalty_sort = (original_diff_abs < self.threshold).float()
        penalty_loss = torch.sum(penalty_sort * torch.abs(reconstructed_diff)) * self.penalty_weight

        total_loss = reconstructed_loss + penalty_loss
        return total_loss
