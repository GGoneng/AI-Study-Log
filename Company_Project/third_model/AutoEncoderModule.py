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

class AutoEncoderDataset(Dataset):
    def __init__(self, featureDF):
        self.featureDF = featureDF
        self.n_rows = self.featureDF.shape[0]
        self.n_cols = self.featureDF.shape[1]

    def __len__(self):
        return self.n_rows
    
    def __getitem__(self, index):
        featureTS = torch.FloatTensor(self.featureDF.iloc[index].values)

        return featureTS, featureTS   
    

class VAEModel(nn.Module):
    def __init__(self, input_size, hidden_dim, latent_dim, n_layers, dropout,
                 bidirectional):
        super().__init__()

        self.encoder = nn.GRU(
            input_size = input_size,
            hidden_size = hidden_dim,
            num_layers = n_layers,
            dropout = dropout,
            bidirectional = bidirectional,
            batch_first = True
        )

        self.mu = nn.Linear(hidden_dim * 2 if bidirectional else hidden_dim, latent_dim)
        self.logvar = nn.Linear(hidden_dim * 2 if bidirectional else hidden_dim, latent_dim)

        self.decoder = nn.GRU(
            input_size = latent_dim,
            hidden_size = hidden_dim,
            num_layers = n_layers,
            dropout = dropout,
            bidirectional = bidirectional,
            batch_first = True
        )
        self.output = nn.Linear(hidden_dim * 2 if bidirectional else hidden_dim, 1)

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        
        return mu + eps * std
    
    def forward(self, inputs):
        encoder, hidden = self.encoder(inputs)
        
        if self.encoder.bidirectional:
            hidden = torch.cat([hidden[-2], hidden[-1]], dim=-1)
        else:
            hidden = hidden[-1]

        mu = self.mu(hidden)
        logvar = self.logvar(hidden)
        
        reparameter = self.reparameterize(mu, logvar)
        reparameter = reparameter.unsqueeze(1)

        decoder, _ = self.decoder(reparameter)

        reconstruction = self.output(decoder)

        return reconstruction, mu, logvar
    



def VAE_loss(reconstruction, target, mu, logvar):
    MAE_loss = nn.L1Loss(reduction = 'mean')
    loss_val = MAE_loss(reconstruction, target)

    kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())

    return loss_val + kl_loss

def testing(featureDF, targetDF, model, DEVICE):
    featureTS = torch.FloatTensor(featureDF.values).unsqueeze(1).to(DEVICE)
    targetTS = torch.FloatTensor(targetDF.values).unsqueeze(1).to(DEVICE)
    
    model.eval()
    
    with torch.no_grad():
        reconstruction, mu, logvar = model(featureTS)
        vae_loss_val = VAE_loss(reconstruction, targetTS, mu, logvar)

    return vae_loss_val


def training(testDF, testtargetDF, model, trainDL,
              optimizer, EPOCH, scheduler, DEVICE, accumulation_steps):
    SAVE_PATH = './saved_models/'
    os.makedirs(SAVE_PATH, exist_ok = True)

    BREAK_CNT_LOSS = 0
    BREAK_CNT_SCORE = 0
    LIMIT_VALUE = 10

    VAE_LOSS_HISTORY = [[], []]

    for epoch in range(1, EPOCH + 1):
        SAVE_MODEL = os.path.join(SAVE_PATH, f'model_{epoch}.pth')
        SAVE_WEIGHT = os.path.join(SAVE_PATH, f'model_weights_{epoch}.pth')

        vae_loss_total = 0

        for step, (featureTS, targetTS) in enumerate(trainDL):
            featureTS = featureTS.unsqueeze(1).to(DEVICE)
            targetTS = targetTS.unsqueeze(1).to(DEVICE)

            # Forward pass
            reconstruction, mu, logvar = model(featureTS)
            vae_loss = VAE_loss(reconstruction, targetTS, mu, logvar)

            # Loss 누적 및 Backward pass
            vae_loss = vae_loss / accumulation_steps  # 누적 단계로 나눔
            vae_loss.backward()
            vae_loss_total += vae_loss.item() * accumulation_steps

            # Accumulation 단계마다 가중치 업데이트
            if (step + 1) % accumulation_steps == 0:
                optimizer.step()
                optimizer.zero_grad()
        

        test_vae_loss = testing(testDF, testtargetDF, model, DEVICE)

        VAE_LOSS_HISTORY[1].append(test_vae_loss)
        VAE_LOSS_HISTORY[0].append(vae_loss_total / len(trainDL))

        print(f'[{epoch} / {EPOCH}]\n- TRAIN VAE LOSS : {VAE_LOSS_HISTORY[0][-1]}')
        print(f'\n- TEST VAE LOSS : {VAE_LOSS_HISTORY[1][-1]}')
        scheduler.step(test_vae_loss)

        if len(VAE_LOSS_HISTORY[1]) >= 2:
            if VAE_LOSS_HISTORY[1][-1] >= VAE_LOSS_HISTORY[1][-2]: BREAK_CNT_LOSS += 1
        
        if len(VAE_LOSS_HISTORY[1]) == 1:
            torch.save(model.state_dict(), SAVE_WEIGHT)
            torch.save(model, SAVE_MODEL)

        else:
            if VAE_LOSS_HISTORY[1][-1] < min(VAE_LOSS_HISTORY[1][:-1]):
                torch.save(model.state_dict(), SAVE_WEIGHT)
                torch.save(model, SAVE_MODEL)

        if BREAK_CNT_LOSS > LIMIT_VALUE:
            print(f"성능 및 손실 개선이 없어서 {epoch} EPOCH에 학습 중단")
            # break

    return VAE_LOSS_HISTORY