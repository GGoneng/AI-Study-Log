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