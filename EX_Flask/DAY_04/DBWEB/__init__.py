from flask import Flask, render_template, request
import torch
import os
import pickle
import re
import numpy as np
from konlpy.tag import Okt
import sys
from DBWEB.models import jong_model
from DBWEB.models import min_model_class

app = Flask(__name__)

MODEL_PATH = r'C:\Users\KDP-2\OneDrive\바탕 화면\FLASK_AI\DAY_04\DBWEB\models'
DATA_PATH = r'C:\Users\KDP-2\OneDrive\바탕 화면\FLASK_AI\DAY_04\DBWEB\data'

MAX_LENGTH = [50, 200]

def load_vocab(vocab_path):
    with open(vocab_path, 'rb') as f:
        vocab = pickle.load(f)
    return {token: idx for idx, token in enumerate(vocab)}

def pad_sequences(sequences, max_length, pad_value):
    sequences = sequences[:max_length]
    pad_length = max_length - len(sequences)
    padded_sequence = sequences + [pad_value] * pad_length
    return np.array([padded_sequence])

def min_preprocessing(text):
    STOP_PATH = os.path.join(DATA_PATH, 'min_stop_words.txt')
    with open(STOP_PATH, 'r', encoding='utf-8') as f:
        stopwords = set([line.strip() for line in f])

    tokenizer = Okt()
    text_tokens = [token for token in tokenizer.morphs(text) if token not in stopwords]

    vocab = load_vocab(os.path.join(MODEL_PATH, 'min_vocab.pkl'))
    unk_id, pad_id = vocab['<unk>'], vocab['<pad>']
    min_ids = [vocab.get(token, unk_id) for token in text_tokens]
    min_ids = pad_sequences(min_ids, MAX_LENGTH[0], pad_id)
    
    return torch.tensor(min_ids, dtype=torch.long)

def load_model(model_class, checkpoint_path, n_vocab, hidden_dim, embedding_dim, n_layers, n_classes):
    model = model_class(
        n_vocab=n_vocab,
        hidden_dim=hidden_dim,
        embedding_dim=embedding_dim,
        n_layers=n_layers,
        n_classes=n_classes
    )
    checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint['model_state_dict'])
    return model


def jong_preprocessing(text):
    STOPWORD_PATH = r'C:\Users\KDP-2\OneDrive\바탕 화면\FLASK_AI\DAY_04\DBWEB\data\basic_ko_stopwords.txt'
    with open(STOPWORD_PATH, 'r', encoding='utf-8') as f:
        stopwords = set([line.strip() for line in f])

    text = re.sub('[^ㄱ-ㅎ가-힣]+',' ',text)

    # 토큰 추출
    tokenizer = Okt()
    
    
    text_tokens = [token for token in tokenizer.morphs(text) if token not in stopwords]

    vocab = load_vocab(r'C:\Users\KDP-2\OneDrive\바탕 화면\FLASK_AI\DAY_04\DBWEB\models\jong_vocab.pkl')
    unk_id, pad_id = vocab['<unk>'], vocab['<pad>']
    jong_ids = [vocab.get(token, unk_id) for token in text_tokens]
    jong_ids = pad_sequences(jong_ids, MAX_LENGTH[1], pad_id)

    return torch.tensor(jong_ids, dtype=torch.long)


@app.route('/', methods=['GET', 'POST'])
def index():
    result = []

    if request.method == 'POST':
        text = request.form['keyword']
        min_ids = min_preprocessing(text)
        
        # Load and use the MinSentenceClassifier model
        min_model_path = r'C:\Users\KDP-2\OneDrive\바탕 화면\FLASK_AI\DAY_04\DBWEB\models\min_model.pth'
        classifier = load_model(
            min_model_class.SentenceClassifier, min_model_path, n_vocab=50002, hidden_dim=64,
            embedding_dim=1024, n_layers=2, n_classes=12
        )
        
        classifier.eval()
        with torch.no_grad():
            logits = classifier(min_ids)
            yhat1 = torch.argmax(logits, dim=1).item()
            result.append(yhat1)


        jong_ids = jong_preprocessing(text)
        jong_classifier = load_model(
            jong_model.SentenceClassifier2, r'C:\Users\KDP-2\OneDrive\바탕 화면\FLASK_AI\DAY_04\DBWEB\models\best_model48.pth',
              n_vocab = 10002, hidden_dim = 64, embedding_dim = 128, n_layers = 2, n_classes = 12
              )
        jong_classifier.eval()
        with torch.no_grad():
            logits = jong_classifier(jong_ids)
            yhat2 = torch.argmax(logits, dim=1).item()
            result.append(yhat2)

    return render_template('index.html', prediction=result)

if __name__ == '__main__':
    app.run(debug=True)