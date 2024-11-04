from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
import torchvision.transforms as transforms
from torchvision.transforms import v2

from sklearn.feature_extraction.text import CountVectorizer

import re
import spacy
import pickle
import numpy as np
import pandas as pd

from gensim.models import Word2Vec

def preprocessing_text(string):
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


def min_preprocessing_img(image):
    preprocess = v2.Compose(
    [
        v2.Resize(size = (256, 256)),
        v2.ToImage(),
        v2.ToDtype(torch.float32, scale = True),
        v2.Normalize(mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225])
    ]
    )

    image_tensor = preprocess(image)

    return image_tensor.unsqueeze(0)


def hyuck_preprocessing_img(image):
    preprocess = v2.Compose(
    [
        v2.Resize(size = (224, 224)),
        v2.ToImage(),
        v2.ToDtype(torch.float32, scale = True),
        v2.Normalize(mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225])
    ]
    )

    image_tensor = preprocess(image)

    return image_tensor.unsqueeze(0)


def hwang_preprocessing_img(image):
    preprocess = v2.Compose(
    [
        v2.Resize(size = (224, 224)),
        v2.ToImage(),
        v2.ToDtype(torch.float32, scale = True),
        v2.Normalize(mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225])
    ]
    )

    image_tensor = preprocess(image)

    return image_tensor.unsqueeze(0)


def joo_preprocessing_img(image):
    preprocess = v2.Compose(
    [
        v2.Resize(size = (224, 224)),
        v2.ToImage(),
        v2.ToDtype(torch.float32, scale = True),
        v2.Normalize(mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225])
    ]
    )

    image_tensor = preprocess(image)

    return image_tensor.unsqueeze(0)


def min_predict_value(input_vectorDF, model_file):
    model = torch.load(model_file, weights_only = False, map_location = torch.device('cpu'))

    return (model(input_vectorDF) >= 0.5).float()


def hyuck_predict_value(input_vectorDF, model_file):
    model = models.vgg16(pretrained=False)
    model.classifier[6] = torch.nn.Linear(4096, 1)
    model.load_state_dict(torch.load(model_file, weights_only = True, map_location = torch.device('cpu')))

    return (model(input_vectorDF) >= 0.5).float()


def hwang_predict_value(input_vectorDF, model_file):
    model = torch.load(model_file, weights_only = False, map_location = torch.device('cpu'))

    return (model(input_vectorDF) >= 0.5).float()


def joo_predict_value(input_vectorDF, model_file):
    model = torch.load(model_file, weights_only = False, map_location = torch.device('cpu'))

    return (model(input_vectorDF) >= 0.5).float()


# 모델 클래스 정의
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


convnext_tiny = models.convnext_tiny(pretrained = True, weights = models.ConvNeXt_Tiny_Weights.IMAGENET1K_V1)


class Custommodel(nn.Module):
    def __init__(self):
        super(Custommodel, self).__init__()
        self.features = convnext_tiny.features
        self.avgpool = convnext_tiny.avgpool
        self.classifier = convnext_tiny.classifier
        self.fc = nn.Sequential(
                nn.ReLU(),
                nn.Linear(1000, 500),
                nn.Dropout(0.25),
                nn.ReLU(),
                nn.Linear(500, 250),
                nn.Dropout(0.25),
                nn.ReLU(),
                nn.Linear(250, 1)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = self.classifier(x)
        x = self.fc(x) 
    
        return F.sigmoid(x)
    
class CustomVgg16Model(nn.Module):
    def __init__(self):
        super(CustomVgg16Model, self).__init__()    # 이러면 전의학습 들고오는가봄
        self.vgg16 = models.vgg16(weights=models.VGG16_Weights.IMAGENET1K_V1)
        self.features = self.vgg16.features
        self.avgpool = self.vgg16.avgpool
        self.classifier = self.vgg16.classifier
        self.custom_layer = nn.Sequential(
            nn.ReLU(),
            nn.Linear(1000, 500),
            nn.ReLU(),
            nn.Linear(500, 50),
            nn.ReLU(),
            nn.Linear(50, 1)
        )
    
    def forward(self, x):
        y = self.features(x)
        y = self.avgpool(y)
        y = torch.flatten(y, 1)
        y = self.classifier(y)
        y = F.sigmoid(self.custom_layer(y))
        
        return y


class VGG16WithFC(nn.Module):
    def __init__(self):
        super(VGG16WithFC, self).__init__()

        self.vgg16 = models.vgg16(pretrained=True)

        self.features = self.vgg16.features
        self.avgpool = self.vgg16.avgpool
        self.classifier = self.vgg16.classifier

        self.extra_fc = nn.Sequential(
            nn.ReLU(),
            nn.Linear(1000,500),
            nn.ReLU(),
            nn.Linear(500,1)
        )

    def forward(self, x):
        x = self.features(x) 
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)  
        x = self.extra_fc(x)  
        return x

def min_preprocessing_text(text):
    TOKEN_MODEL = 'ko_core_news_lg'
    nlp = spacy.load(TOKEN_MODEL)

    token_list = []
    doc = nlp(text)

    for token in doc:
        if (not token.is_punct) and (not token.is_stop) and (not token.is_space):
            token_list.append(str(token))
    
    with open(r'C:\Users\KDP-2\OneDrive\바탕 화면\Python\EX_NLP\DAY_05\WEB\cgi-bin\vocab_min.pkl', 'rb') as f:
        vocab = pickle.load(f)

    PAD_TOKEN, OOV_TOKEN = 'pad', 'oov'

    encoded_data = []

    for token in token_list:
        if token in vocab:
            encoded_data.append(vocab[token])
        else:
            encoded_data.append(vocab[OOV_TOKEN])
    
    MAX_LENGTH = 20

    current_length = len(encoded_data)

    if current_length < MAX_LENGTH:
        encoded_data = encoded_data + ([vocab[PAD_TOKEN]] * (MAX_LENGTH - current_length))
    else:
        encoded_data = encoded_data[ : MAX_LENGTH]

    dataTS = torch.LongTensor([encoded_data])

    return dataTS


    # word2vec = Word2Vec.load('word2vec_이민하.model')

    # n_vocab = len(vocab)
    # embedding_dim = 100

    # init_embeddings = np.zeros((n_vocab, embedding_dim))    

    # for token, index in vocab.items():
    #     if token not in [PAD_TOKEN, OOV_TOKEN]:
    #         init_embeddings[index] = word2vec.wv[token]

# 문장 분류 모델 

class SentenceClassifier(nn.Module):
    def __init__(self,
                 n_vocab,
                 hidden_dim,
                 embedding_dim,
                 n_layers,
                 dropout = 0.5,
                 # 양방향은 빈칸에 들어갈 단어를 고르는 등, 앞 문장과 뒷 문장이 둘 다 중요할 때 사용
                 bidirectional = True,
                 model_type = 'lstm',
                 pretrained_embedding = None
                 ):
        super().__init__()

        if pretrained_embedding is not None:
            self.embedding = nn.Embedding.from_pretrained(
                torch.tensor(pretrained_embedding, dtype = torch.float32)
            )
        else:
            self.embedding = nn.Embedding(
                num_embeddings = n_vocab,
                embedding_dim = embedding_dim,
                padding_idx = 0
        )
        
        if model_type == 'rnn':
            self.model = nn.RNN(
                input_size = embedding_dim,
                hidden_size = hidden_dim,
                num_layers = n_layers,
                bidirectional = bidirectional,
                dropout = dropout,
                batch_first = True
            )
        elif model_type == 'lstm':
            self.model = nn.LSTM(
                input_size = embedding_dim,
                hidden_size = hidden_dim,
                num_layers = n_layers,
                bidirectional = bidirectional,
                dropout = dropout,
                batch_first = True
            )
        
        if bidirectional:
            self.classifier = nn.Linear(hidden_dim * 2, 1)

        else:
            self.classifier = nn.Linear(hidden_dim, 1)

        self.dropout = nn.Dropout(dropout)

    def forward(self, inputs):
        embeddings = self.embedding(inputs)
        output, _ = self.model(embeddings)
        last_output = output[:, -1, :]
        last_output = self.dropout(last_output)
        logits = self.classifier(last_output)
        return F.sigmoid(logits)