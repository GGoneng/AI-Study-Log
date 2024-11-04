from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

import torch
import torch.nn as nn
import torch.nn.functional as F

from sklearn.feature_extraction.text import CountVectorizer

import re

def preprocessing(string):
    stop_words = set(stopwords.words('english'))

    string = re.sub(r'[^a-z\s]', '', string.lower())
    string_list = word_tokenize(string)

    word_list = []

    for word in string_list:
        if word not in stop_words:
            word_list.append(word)
    
    stemmer = PorterStemmer()

    i = 0

    for word in word_list:
        word_list[i] = stemmer.stem(word)
        i += 1
    
    return word_list



class BCFModel(nn.Module):

    def __init__(self, in_in, in_out, out_out, h_ins = [], h_outs = [], dropout_prob = 0.5):
        super().__init__()

        self.in_layer = nn.Linear(in_in, h_ins[0] if len(h_ins) else in_out)
        self.dropout = nn.Dropout(p = dropout_prob)
        
        self.h_layers = nn.ModuleList()
        for idx in range(len(h_ins) - 1):
            self.h_layers.append(nn.Linear(h_ins[idx], h_outs[idx + 1]))
            self.h_layers.append(nn.Dropout(p = dropout_prob))

        self.out_layer = nn.Linear(h_outs[-1] if len(h_outs) else in_out, out_out)

    def forward(self, input_data):

        y = F.relu(self.in_layer(input_data))
        y = self.dropout(y)
        for linear in self.h_layers:
            y = F.relu(linear(y))
            y = self.dropout(y)
        return F.sigmoid(self.out_layer(y))

def predict_value(input_vectorDF, model):
    test_inputTS = torch.FloatTensor(input_vectorDF.values)

    return (model(test_inputTS) >= 0.5).float()