import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from torchvision.transforms import v2

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


def min_predict_value(input_vectorDF, model_file):
    model = torch.load(model_file, weights_only = False, map_location = torch.device('cpu'))

    return (model(input_vectorDF) >= 0.5).float()