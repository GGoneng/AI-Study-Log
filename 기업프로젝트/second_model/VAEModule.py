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
    

class VAEModel(nn.Module):
    def __init__(self, input_size, hidden_dim, latent_dim):
        super().__init__()

        self.encoder = nn.Sequential(
            nn.Linear(input_size, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU()
        )

        self.mu = nn.Linear(hidden_dim, latent_dim)
        self.logvar = nn.Linear(hidden_dim, latent_dim)

        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_size)
        )
 
    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        
        return mu + eps * std
    
    def forward(self, inputs):
        encode = self.encoder(inputs)
        mu = self.mu(encode)
        logvar = self.logvar(encode)
        
        reparameter = self.reparameterize(mu, logvar)

        reconstruction = self.decoder(reparameter)

        return reconstruction, mu, logvar
    



def VAE_loss(reconstruction, target, mu, logvar):
    MAE_loss = nn.MSELoss(reduction = 'sum')
    loss_val = MAE_loss(reconstruction, target)

    kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())

    return loss_val + kl_loss

def testing(featureDF, targetDF, model, DEVICE):
    featureTS = torch.FloatTensor(featureDF.values).to(DEVICE)
    targetTS = torch.FloatTensor(targetDF.values).to(DEVICE)
    
    model.eval()
    
    with torch.no_grad():
        reconstruction, mu, logvar = model(featureTS)
        vae_loss_val = VAE_loss(reconstruction, targetTS, mu, logvar)

    return vae_loss_val

def training(model, trainDL, optimizer, 
             EPOCH, scheduler, DEVICE):
    
    SAVE_PATH = './saved_models/'
    os.makedirs(SAVE_PATH, exist_ok = True)

    BREAK_CNT_LOSS = 0
    BREAK_CNT_SCORE = 0

    VAE_LOSS_HISTORY = []

    for epoch in range(1, EPOCH + 1):
        model.train()
        SAVE_MODEL = os.path.join(SAVE_PATH, f'model_{epoch}.pth')
        SAVE_WEIGHT = os.path.join(SAVE_PATH, f'model_weights_{epoch}.pth')

        vae_loss_total = 0

        for featureTS, targetTS in trainDL:
            featureTS = featureTS.to(DEVICE)
            targetTS = targetTS.to(DEVICE)

            # Forward pass
            reconstruction, mu, logvar = model(featureTS)
            vae_loss = VAE_loss(reconstruction, targetTS, mu, logvar)
            
            vae_loss_total += vae_loss.item()
           
            optimizer.zero_grad()
        
            vae_loss.backward()
        
            optimizer.step()

        VAE_LOSS_HISTORY.append(vae_loss_total / len(trainDL))
        train_vae_loss = (vae_loss_total / len(trainDL))
        print(f'[{epoch} / {EPOCH}]\n- TRAIN VAE LOSS : {VAE_LOSS_HISTORY[-1]}')

        scheduler.step(train_vae_loss)

        if len(VAE_LOSS_HISTORY) >= 2:
            if VAE_LOSS_HISTORY[-1] >= VAE_LOSS_HISTORY[-2]: BREAK_CNT_LOSS += 1
        
        if len(VAE_LOSS_HISTORY) == 1:
            torch.save(model.state_dict(), SAVE_WEIGHT)
            torch.save(model, SAVE_MODEL)

        else:
            if VAE_LOSS_HISTORY[-1] < min(VAE_LOSS_HISTORY[:-1]):
                torch.save(model.state_dict(), SAVE_WEIGHT)
                torch.save(model, SAVE_MODEL)


    return VAE_LOSS_HISTORY