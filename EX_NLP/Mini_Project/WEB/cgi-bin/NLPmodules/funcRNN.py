#------------------------------------------------------------------------------------------
# 모듈 로딩
#------------------------------------------------------------------------------------------

# 파이썬 내장 모듈
from collections import Counter

# 데이터분석 관련 모듈
import pandas as pd
import numpy as np

# Pytorch 모듈
import torch

#------------------------------------------------------------------------------------------
# 사용자 정의 함수
#------------------------------------------------------------------------------------------

# 데이터 토큰화 및 단어 사전 구축
def build_vocab(corpus, n_vocab, special_tokens):
    counter = Counter()
    for tokens in corpus:
        counter.update(tokens)
    vocab = special_tokens

    for token, count in counter.most_common(n_vocab):
        vocab.append(token)
    return vocab

# 정수 인코딩 및 패딩 진행 함수
def pad_sequences(sequences, max_length, pad_value):
    result = list()
    for sequence in sequences:
        sequence = sequence[:max_length]
        pad_length = max_length - len(sequence)
        padded_sequence = sequence + [pad_value] * pad_length
        result.append(padded_sequence)
    return np.asarray(result)

# 모델 학습 함수
def trainModel(model, datasets, criterion, optimizer, device, interval):
    model.train()
    losses = list()

    for step, (input_ids, labels) in enumerate(datasets):
        input_ids = input_ids.to(device).squeeze(1)
        labels = labels.to(device)

        logits = model(input_ids)
        loss = criterion(logits, labels)
        losses.append(loss.item())

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if step % interval == 0:
            print(f'Train Loss {step}: {np.mean(losses)}')

# 모델 테스트 함수
def testModel(model, datasets, criterion, device):
    model.eval()
    losses = list()
    corrects = list()

    for step, (input_ids, labels) in enumerate(datasets):
        input_ids = input_ids.to(device)
        labels = labels.to(device).unsqueeze(1)

        logits = model(input_ids)
        loss = criterion(logits, labels)
        losses.append(loss.item())
        yhat = torch.sigmoid(logits)>.5
        corrects.extend(
            torch.eq(yhat, labels).cpu().tolist()
        )
    print(f'Val Loss : {np.mean(losses)}, Val Accuracy : {np.mean(corrects)}')

#------------------------------------------------------------------------------------------
# 한국어 불용어 제거 함수
#------------------------------------------------------------------------------------------

# def remove_stopwords(tokens):
#     return [token for token in tokens if token not in stopwords]


#------------------------------------------------------------------------------------------
# 제너레이터 활용 함수
#------------------------------------------------------------------------------------------

def generateToken(dataset, load):
    for text, label in dataset:
        token_list = []
        doc = load(text)

        for token in doc:
            if (not token.is_punct) and (not token.is_stop):
                token_list.append(str(token))
        yield token_list

# ---------------------------------------------------------------------
# 함수 이름 : predict_model()
# 함수 역할 : 모델 예측 함수
# 매개 변수 : model, data
# ---------------------------------------------------------------------

def predict_model(model, data, vocab, max_length):
    # 데이터가 문자열이라면 토큰화 및 인덱스로 변환
    tokens = [vocab.get(token, vocab['oov']) for token in data]  # 토큰을 인덱스로 변환

    # 패딩하여 모델의 입력 형태와 일치시키기
    if len(tokens) < max_length:
        tokens = tokens + [vocab['pad']] * (max_length - len(tokens))
    else:
        tokens = tokens[:max_length]

    dataTS = torch.LongTensor(tokens).unsqueeze(0)

    # 검증 모드로 모델 설정
    model.eval()
    with torch.no_grad():
        # 추론/평가
        logits = model(dataTS)
        pre_val = torch.sigmoid(logits)

    prediction = (pre_val >= 0.5).float()

    return prediction.item()