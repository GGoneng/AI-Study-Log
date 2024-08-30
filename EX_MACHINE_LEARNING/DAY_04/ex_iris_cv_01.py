"""
붓꽃 품종 분류
- 목표 : 붓꽃의 3개 품종을 분류하기
- 데이터셋 : 내장 데이터셋
- 피쳐 : 4개
- 타겟 : 품종 1개
- 학습 : 지도학습 > 분류
"""

# [1] 데이터 준비
# 모듈 로딩
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# 내장 데이터셋 로딩
data = load_iris(as_frame = True)

# Bunch 인스턴스 => dict와 유사한 형태
print(f"data's keys : \n{data.keys()} \n\n")

featureDF = data["data"]
targetSR = data["target"]

print(f"feature Data's shape : {featureDF.shape}")
print(f"target Data's shape : {targetSR.shape}\n\n")

print(f"feature Data's head : \n{featureDF.head(1)}")
print(f"target Data's head : \n{targetSR.head(1)}\n\n")

# [2] 학습을 위한 데이터 셋 준비 => 학습용, 검증용, 테스트용
# 학습용 & 테스트용 분리
X_train, X_test, y_train, y_test = train_test_split(featureDF,
                                                    targetSR,
                                                    stratify = targetSR)

# 학습용 & 검증용 분리
X_train, X_val, y_train, y_val = train_test_split(X_train,
                                                    y_train,
                                                    stratify = y_train)

print(f"Train DS : {X_train.shape[0]}  {X_train.shape[0]/featureDF.shape[0]:.2f}%")
print(f"Val DS : {X_val.shape[0]}  {X_val.shape[0]/featureDF.shape[0]:.2f}%")
print(f"Test DS : {X_test.shape[0]}  {X_test.shape[0]/featureDF.shape[0]:.2f}%\n\n")

# [3] 교차 검증 방식
# 모듈 로딩
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.tree import DecisionTreeClassifier

# 모델 인스턴스 생성
dtc_model = DecisionTreeClassifier()


# [3-1] KFold 기반 ---------------------------
# 정확도 저장 리스트
accuracys = []

# KFold 인스턴스 생성 [기본 k = 5]
kfold = KFold()

# K번 만큼 K개 데이터셋으로 학습 진행
# -> K등분 후 학습용 데이터셋 인덱스, 검증용 데이터셋 인덱스
for idx, (train_index, val_index) in enumerate(kfold.split(featureDF)):
    # print(F"train_index : {train_index.tolist()}")

    # X_train, X_val 데이터셋 설정
    X_train, y_train = featureDF.iloc[train_index.tolist()], targetSR[train_index.tolist()]
    X_val, y_val = featureDF.iloc[val_index.tolist()], targetSR[val_index.tolist()]

    # 학습 진행
    dtc_model.fit(X_train, y_train)

    # 평가 => 분류의 경우 score() 메서드 => 정확도 반환
    train_acc = dtc_model.score(X_train, y_train)
    val_acc = dtc_model.score(X_val, y_val)
    accuracys.append([train_acc, val_acc])

    print(f"[{idx}번째] Train 정확도 : {train_acc}  Val 정확도 : {val_acc}")  

# 평균 계산
train_mean = sum([value[0] for value in accuracys]) / kfold.n_splits
test_mean = sum([value[1] for value in accuracys]) / kfold.n_splits

print(f"\n\nTrain 정확도 : {train_mean}    Val 정확도 : {test_mean:.2f}")


# => [3-2] StraitifiedKFold : 정답 / 레이블 / 타겟의 비율을 고려해서 데이터 나눔

accuracys = []

# KFold 인스턴스 생성 [기본 k = 5]
skFold = StratifiedKFold()

# K번 만큼 K개 데이터셋으로 학습 진행
# -> K등분 후 학습용 데이터셋 인덱스, 검증용 데이터셋 인덱스
for idx, (train_index, val_index) in enumerate(skFold.split(featureDF, targetSR), 1):
    # print(F"train_index : {train_index.tolist()}")

    # X_train, X_val 데이터셋 설정
    X_train, y_train = featureDF.iloc[train_index.tolist()], targetSR[train_index.tolist()]
    X_val, y_val = featureDF.iloc[val_index.tolist()], targetSR[val_index.tolist()]

    # 학습 진행
    dtc_model.fit(X_train, y_train)

    # 평가 => 분류의 경우 score() 메서드 => 정확도 반환
    train_acc = dtc_model.score(X_train, y_train)
    val_acc = dtc_model.score(X_val, y_val)
    accuracys.append([train_acc, val_acc])

    print(f"[{idx}번째] Train 정확도 : {train_acc}  Val 정확도 : {val_acc}")  

# 평균 계산
train_mean = sum([value[0] for value in accuracys]) / skFold.n_splits
test_mean = sum([value[1] for value in accuracys]) / skFold.n_splits

print(f"\n\nTrain 정확도 : {train_mean}    Val 정확도 : {test_mean:.2f}\n\n")


# 교차 검증 및 성능 평가 동시 진행 함수 
#  => cross_val_score, cross_val_predict
#  => cross_validate

from sklearn.model_selection import cross_val_predict, cross_val_score, cross_validate 


# [1] 전체 DS ==> 학습용과 테스트용 DS 분리
X_train, X_test, y_train, y_test = train_test_split(featureDF, 
                                                    targetSR, 
                                                    stratify = targetSR)


# cross_val_predict
predict = cross_val_predict(dtc_model, X_train, y_train, cv = 3)

print(f"predict : {predict}\n\n")


# cross_val_score
print(cross_val_score(dtc_model, X_train, y_train), "\n\n")

# cross_validata
result = cross_validate(dtc_model, X_train, y_train,
                        return_train_score = True,
                        return_estimator = True)

resultDF = pd.DataFrame(result).loc[:, ["test_score", "train_score"]]
print(resultDF, "\n\n")

# - 최적화된 모델 추출
best_model = result['estimator'][2]

# 테스트 데이터로 확인
print(best_model.predict(X_test), "\n\n")
print(best_model.score(X_test, y_test), "\n\n")