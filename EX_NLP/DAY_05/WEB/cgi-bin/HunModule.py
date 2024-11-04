#------------------------------------------------------------------------------------------
# 모듈 로딩
#------------------------------------------------------------------------------------------
from torch import nn
import torch
from torch.utils.data import Dataset, DataLoader
from konlpy.tag import Kkma
import pickle

#------------------------------------------------------------------------------------------
# 문장 분류 모델 정의
#------------------------------------------------------------------------------------------

class SentenceClassifier(nn.Module):
    def __init__(self,
                 n_vocab,
                 hidden_dim,
                 embedding_dim,
                 n_layers,
                 dropout=0.5,
                 bidirectional=True,
                 model_type='lstm'
                 ):
        super().__init__()

        self.embedding = nn.Embedding(
            num_embeddings=n_vocab,
            embedding_dim=embedding_dim,
            padding_idx=0
        )
        if model_type == 'rnn':
            self.model = nn.RNN(
                input_size=embedding_dim,
                hidden_size=hidden_dim,
                num_layers=n_layers,
                bidirectional=bidirectional,
                dropout=dropout,
                batch_first=True,
            )
        elif model_type == 'lstm':
            self.model = nn.LSTM(
                input_size=embedding_dim,
                hidden_size=hidden_dim,
                num_layers=n_layers,
                bidirectional=bidirectional,
                dropout=dropout,
                batch_first=True,
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
        return logits
    
def hun_preprocessing_text(text):
    kkma = Kkma()
    doc = kkma.morphs(text)

    with open(r'C:\Users\KDP-2\OneDrive\바탕 화면\Python\EX_NLP\DAY_05\WEB\cgi-bin\vocab_hun.pkl', 'rb') as f:
        vocab = pickle.load(f)     

    # 불용어 경로
    STOPWORDS = r'C:\Users\KDP-2\OneDrive\바탕 화면\Python\EX_NLP\DAY_05\WEB\cgi-bin\stopwords-ko_hun.txt'
    with open(STOPWORDS, mode='r', encoding='utf-8') as f:
        stopwords_ko = f.read().splitlines()

    token_list = []

    for token in doc:
        if (not token in stopwords_ko):
            token_list.append(str(token))

    PAD_TOKEN, OOV_TOKEN = 'pad', 'oov'

    encoded_data = []

    for token in token_list:
        if token in vocab:
            encoded_data.append(vocab[token])
        else:
            encoded_data.append(vocab[OOV_TOKEN])

    MAX_LENGTH = 50

    current_length = len(encoded_data)

    if current_length < MAX_LENGTH:
        encoded_data = encoded_data + ([vocab[PAD_TOKEN]] * (MAX_LENGTH - current_length))
    else:
        encoded_data = encoded_data[ : MAX_LENGTH]
    
    dataTS = torch.LongTensor([encoded_data])

    return dataTS

def hun_predict_value(input_vectorDF, model_file):
    model = torch.load(model_file, weights_only = False, map_location = torch.device('cpu'))

    return (model(input_vectorDF) >= 0.5).float()