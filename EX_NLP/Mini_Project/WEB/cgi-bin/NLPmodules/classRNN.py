#------------------------------------------------------------------------------------------
# 모듈 로딩
#------------------------------------------------------------------------------------------
from torch import nn
import torch
from torch.utils.data import Dataset, DataLoader

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
    
#------------------------------------------------------------------------------------------
# 문장 분류 모델 정의2 (사전 학습된 임베딩 계층 적용)
#------------------------------------------------------------------------------------------

class SentenceClassifier2(nn.Module):
    def __init__(self,
                 n_vocab,
                 hidden_dim,
                 embedding_dim,
                 n_layers,
                 dropout=0.5,
                 bidirectional=True,
                 model_type='lstm',
                 pretrained_embedding=None
                 ):
        super().__init__()

        self.embedding = nn.Embedding(
            num_embeddings=n_vocab,
            embedding_dim=embedding_dim,
            padding_idx=0
        )
        if pretrained_embedding is not None:
            self.embedding = nn.Embedding.from_pretrained(
                torch.tensor(pretrained_embedding, dtype=torch.float32)
            )
        else:
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

#------------------------------------------------------------------------------------------
# 텍스트 커스텀 데이터셋
#------------------------------------------------------------------------------------------
class TextDataset(Dataset):
    def __init__(self, feature, label):
        self.feature = feature
        self.label = label
        self.n_rows = feature.shape[0]

    def __len__(self):
        return self.n_rows
    
    def __getitem__(self, index):
        return self.feature.iloc[index], self.label.iloc[index]

class TextDataset2(Dataset):
    def __init__(self, feature, label):
        self.feature = feature
        self.label = label
        self.n_rows = feature.shape[0]

    def __len__(self):
        return self.n_rows
    
    def __getitem__(self, index):
        return torch.FloatTensor(self.feature.iloc[index]), torch.LongTensor(self.label.iloc[index])

#------------------------------------------------------------------------------------------
# LSTM 커스텀 데이터셋
#------------------------------------------------------------------------------------------

### ===> LSTM 모델 정의
class LSTMModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, num_layers):
        super(LSTMModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x):
        x = self.embedding(x)
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])  # 마지막 시퀀스 출력만 사용
        return out
