# -----------------------------------------------------------------------------------
# 파일명       : GRUAutoEncoderModule.py
# 설명         : AutoEncoder 모델 학습을 위한 모듈              
# 작성자       : 이민하
# 작성일       : 2024-11-27
# 
# 사용 모듈    :
# - os                               # 경로 관리
# - torch, torch.nn                  # PyTorch 모델 구축 및 연산
# - torch.utils.data                 # 데이터셋 처리
# - sklearn.preprocessing            # 데이터 정규화 및 스케일링
# - torchmetrics.regression          # 회귀 모델 평가 지표 계산
# -----------------------------------------------------------------------------------
# >> 주요 기능
# - 모델의 학습과 평가를 위한 모듈
#
# >> 업데이트 내역
# [2024-11-27] MLP 구조의 Vanilla AutoEncoder 모델 클래스 및 학습, 평가 함수 생성
#              Custom Loss 생성
# [2024-11-30] VAE AutoEncoder 모델 클래스 및 학습, 평가 함수 생성 (성능 저하)
# [2024-12-03] Recurrent AutoEncoder 모델 클래스 및 학습, 평가 함수 생성 (성능 저하)
# [2024-12-09] GRU AutoEncoder 모델 클래스 및 학습, 평가 함수 생성
# -----------------------------------------------------------------------------------

# 경로 관리
import os

# PyTorch 모델 구축 및 연산
import torch
import torch.nn as nn

# 데이터셋 처리
from torch.utils.data import Dataset

# 데이터 정규화 및 스케일링
from sklearn.preprocessing import MinMaxScaler, RobustScaler

# 회귀 모델 평가 지표 계산
from torchmetrics.regression import MeanSquaredError


# 모델 연산을 위한 데이터셋 
class CustomDataset(Dataset):
    def __init__(self, featureDF):
        self.featureDF = featureDF
        self.n_rows = self.featureDF.shape[0]
        self.n_cols = self.featureDF.shape[1]

    def __len__(self):
        return self.n_rows
    
    def __getitem__(self, index):
        featureTS = torch.FloatTensor(self.featureDF.iloc[index].values)

        return featureTS, featureTS       
    
# GRU를 활용한 AutoEncoder 모델
#
# AutoEncoder 모델
# - 입력 데이터를 압축하고, 다시 원래 형태로 복원
# - input_size 보다 latent_dim이 작아야 함
class GRUAutoEncoderModel(nn.Module):
    def __init__(self, input_size, latent_dim, n_layers):
        super().__init__()

        # 인코더 - 압축
        self.encoder = nn.GRU(
            input_size = input_size,
            hidden_size = latent_dim,
            num_layers = n_layers,
            batch_first = True
        )

        # self.latent_layer = nn.Linear(hidden_dim, latent_dim)

        # 디코더 - 복원
        self.decoder = nn.GRU(
            input_size = latent_dim,
            hidden_size = input_size,
            num_layers = n_layers,
            batch_first = True
        )
        
        # 출력층 - 재구성
        self.output_layer = nn.Linear(input_size, input_size)

    def forward(self, inputs):
        # (batch, input_size) -> (batch, 1, input_size)
        inputs = inputs.unsqueeze(1)

        # GRU를 통과 시킨 hidden state 추출
        _, encoder = self.encoder(inputs)

        # 마지막 hidden state 추출
        encoder = encoder[-1]

        decoder, _ = self.decoder(encoder)

        # 출력층을 통해 결과 생성
        reconstruction = self.output_layer(decoder.squeeze(1))

        return reconstruction
    
# 모델 Test 함수
def testing(featureDF, targetDF, model, DEVICE):
    # Pytorch 학습을 위해 데이터프레임 -> 텐서 전환
    featureTS = torch.FloatTensor(featureDF.values).to(DEVICE)
    targetTS = torch.FloatTensor(targetDF.values).to(DEVICE)

    # Dropout, BatchNorm 등 가중치 규제 비활성화    
    model.eval()
    
    # 평가를 위해 역전파 계산 X
    with torch.no_grad():
        decoder = model(featureTS)
        loss_val = MeanSquaredError()(decoder, targetTS)

    return loss_val

# 모델 Train 함수
def training(model, trainDL, optimizer, penalty, threshold,
             EPOCH, scheduler, DEVICE):

    # 가중치 파일 저장 위치 정의    
    SAVE_PATH = './saved_models/'
    os.makedirs(SAVE_PATH, exist_ok = True)

    # Early Stopping을 위한 변수
    BREAK_CNT_LOSS = 0
    BREAK_CNT_SCORE = 0

    # Loss가 더 낮은 가중치 파일을 저장하기 위하여 Loss 로그를 담을 리스트
    LOSS_HISTORY = []

    for epoch in range(1, EPOCH + 1):
        # GPU 환경에서 training과 testing을 반복하므로 eval 모드 -> train 모드로 전환
        # testing에서는 train 모드 -> eval 모드
        model.train()

        SAVE_MODEL = os.path.join(SAVE_PATH, f'model_{epoch}.pth')
        SAVE_WEIGHT = os.path.join(SAVE_PATH, f'model_weights_{epoch}.pth')

        loss_total = 0

        # Train DataLoader에 저장된 feature, target 텐서로 학습 진행
        for featureTS, targetTS in trainDL:
            featureTS = featureTS.to(DEVICE)
            targetTS = targetTS.to(DEVICE)

            # 결과 추론
            reconstructed = model(featureTS)
            # 추론값으로 Loss값 계산
            loss = CustomPenaltyLoss(penalty, threshold)(reconstructed, targetTS)
            
            loss_total += loss.item()
           
            # 이전 gradient 초기화
            optimizer.zero_grad()
        
            # 역전파로 gradient 계산
            loss.backward()
        
            # 계산된 gradient로 가중치 업데이트
            optimizer.step()

            # 위의 3줄이 딥러닝의 기본 원리 :
            # 1. 이전에 계산된 gradient 초기화
            # 2. 역전파를 통해 gradient 계산
            # 3. 계산된 gradient를 통해 가중치 업데이트

        LOSS_HISTORY.append(loss_total / len(trainDL))
        train_loss = (loss_total / len(trainDL))
        print(f'[{epoch} / {EPOCH}]\n- TRAIN LOSS : {LOSS_HISTORY[-1]}')

        print(targetTS[0])
        print(reconstructed[0])

        # 스케줄러 업데이트 (Loss 값 최소화)
        scheduler.step(train_loss)

        # Early Stopping 구현
        if len(LOSS_HISTORY) >= 2:
            if LOSS_HISTORY[-1] >= LOSS_HISTORY[-2]: BREAK_CNT_LOSS += 1
        
        if len(LOSS_HISTORY) == 1:
            torch.save(model.state_dict(), SAVE_WEIGHT)
            torch.save(model, SAVE_MODEL)

        else:
            if LOSS_HISTORY[-1] < min(LOSS_HISTORY[:-1]):
                torch.save(model.state_dict(), SAVE_WEIGHT)
                torch.save(model, SAVE_MODEL)


    return LOSS_HISTORY

# Custom 손실 함수 생성
# 데이터 특성상 변화량이 거의 없으면, 이상 상황 발생이라는 전제
# 변화량이 거의 없는 데이터에 패널티 적용
# AutoEncoder는 이상 상황에 대한 학습이 미흡하여, 정상 상황일때의 패턴만 추론
# 따라서, AutoEncoder가 추론한 패턴과 데이터 값이 유사하지 않다면, 이상 상황일 확률 높음
class CustomPenaltyLoss(nn.Module):
    def __init__(self, penalty_weight, threshold):
        super().__init__()
        self.penalty_weight = penalty_weight
        self.threshold = threshold
        self.mse_loss = nn.MSELoss()

    def forward(self, original, reconstructed):
        reconstructed_loss = self.mse_loss(reconstructed, original)

        # 데이터 변화량 계산
        original_diff = original[:, 1:] - original[:, :-1]
        reconstructed_diff = reconstructed[:, 1:] - reconstructed[:, :-1]
        original_diff_abs = torch.abs(original_diff)

        # 데이터의 변화량이 threshold보다 적다면, 패널티 적용
        penalty_sort = (original_diff_abs < self.threshold).float()
        penalty_loss = torch.sum(penalty_sort * torch.abs(reconstructed_diff)) * self.penalty_weight

        total_loss = reconstructed_loss + penalty_loss
        return total_loss
