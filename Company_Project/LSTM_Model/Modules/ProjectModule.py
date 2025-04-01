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

    def forward(self, inputs):
        output, _ = self.model(inputs)
        logits = self.linear(output)

        return logits
    
def preprocessing(inputs, scaler_path):
    dataframe = pd.DataFrame(columns = range(28))
    dataframe.loc[0] = inputs

    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)

    scaled_dataframe = scaler.transform(dataframe)

    featureTS = torch.FloatTensor(scaled_dataframe)

    return featureTS

def load_water_model(model_file_path):
    input_size = 28
    hidden_dim = 128
    n_layers = 2
    dropout = 0.9
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

    water_lstm_model = LSTMModel(input_size = input_size, hidden_dim = hidden_dim, 
                             n_layers = n_layers, dropout = dropout, bidirectional = True).to(DEVICE)
    
    water_lstm_model.load_state_dict(torch.load(model_file_path, map_location = torch.device(DEVICE), weights_only = True))
    water_lstm_model.eval()

    return water_lstm_model

def load_electric_model(model_file_path):
    input_size = 28
    hidden_dim = 32
    n_layers = 2
    dropout = 0.9
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

    electric_lstm_model = LSTMModel(input_size = input_size, hidden_dim = hidden_dim, 
                             n_layers = n_layers, dropout = dropout, bidirectional = True).to(DEVICE)
    
    electric_lstm_model.load_state_dict(torch.load(model_file_path, map_location = torch.device(DEVICE), weights_only = True))
    electric_lstm_model.eval()

    return electric_lstm_model

def predict_values(water_model, electric_model, water_TS, electric_TS):

    water_predict_value = water_model(water_TS)
    electric_predict_value = electric_model(electric_TS)

    return water_predict_value.item(), electric_predict_value.item()
