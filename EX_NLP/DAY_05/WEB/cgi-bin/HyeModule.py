from torch import nn
from konlpy.tag import Okt
import pickle
import numpy as np
import torch

class SentenceClassifier(nn.Module):

    def __init__(   self,
                    n_vocab, 
                    hidden_dim,
                    embedding_dim,
                    n_layers,
                    dropout=0.50,
                    bidirectional=True,
                    model_type="lstm"):
        
        super().__init__()
        self.embedding=nn.Embedding(    num_embeddings=n_vocab, 
                                        embedding_dim=embedding_dim,
                                        padding_idx=0)
        if model_type == "rnn":
            self.model=nn.RNN(      input_size=embedding_dim, 
                                    hidden_size=hidden_dim,
                                    num_layers=n_layers,
                                    bidirectional=bidirectional,
                                    dropout=dropout,
                                    batch_first=True,)
        elif model_type =="lstm":
            self.model= nn.LSTM(    input_size=embedding_dim,
                                    hidden_size=hidden_dim,
                                    num_layers=n_layers,
                                    bidirectional=bidirectional,
                                    dropout=dropout,
                                    batch_first=True,)
        
        if bidirectional:
            self.classifier = nn.Sequential(
                nn.Linear(hidden_dim * 2, 200),
                nn.ReLU(),
                nn.Linear(200, 150),
                nn.Dropout(dropout),
                nn.ReLU(),
                nn.Linear(150, 100),
                nn.Dropout(dropout),
                nn.ReLU(),
                nn.Linear(100, 50),
                nn.Dropout(dropout),
                nn.ReLU(),
                nn.Linear(50, 30),
                nn.Dropout(dropout),
                nn.ReLU(),
                nn.Linear(30, 1)
            )        
        else: 
            self.classifier = nn.Sequential(
                nn.Linear(hidden_dim * 2, 200),
                nn.ReLU(),
                nn.Linear(200, 150),
                nn.Dropout(dropout),
                nn.ReLU(),
                nn.Linear(150, 100),
                nn.Dropout(dropout),
                nn.ReLU(),
                nn.Linear(100, 50),
                nn.Dropout(dropout),
                nn.ReLU(),
                nn.Linear(50, 30),
                nn.Dropout(dropout),
                nn.ReLU(),
                nn.Linear(30, 1)
            )
        self.dropout = nn.Dropout(dropout)

    def forward(self, inputs):
        embeddings = self.embedding(inputs)
        output, _ = self.model(embeddings)
        last_output = output[:, -1, :]
        last_output = self.dropout(last_output)
        logits = self.classifier(last_output)
        return logits

def pad_sequences(sequence, max_length, pad_value):

    sequence = sequence[:max_length]
    pad_length = max_length - len(sequence)
    padded_sequence = sequence + [pad_value]*pad_length

    return np.asarray(padded_sequence)

def hye_preprocessing_text(text):
    tokenizer = Okt()
    token_list = tokenizer.morphs(text)

    with open(r'C:\Users\KDP-2\OneDrive\바탕 화면\Python\EX_NLP\DAY_05\WEB\cgi-bin\vocab_hyelee.pkl', 'rb') as f:
        vocab = pickle.load(f)  

    unk_id = vocab["<unk>"]
    encoded_list = [vocab.get(token, unk_id) for token in token_list]
    
    MAX_LENGTH = 32
    pad_id = vocab["<pad>"]
    ids = pad_sequences(encoded_list, MAX_LENGTH, pad_id)

    dataTS = torch.LongTensor([ids])
    return dataTS

def hye_predict_value(input_vectorDF, model_file):
    model = torch.load(model_file, weights_only = False, map_location = torch.device('cpu'))

    return (model(input_vectorDF) >= 0.5).float()