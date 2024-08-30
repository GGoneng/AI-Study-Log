"""
생선 분류 - 최적의 K 찾기 : 하이퍼 파라미터
- 데이터셋 : fish.csv
- 피쳐 / 특성 : Weight, Length
- 타겟 / 라벨 : Species
- 학습 방법 : 지도 학습 => 분류
- 학습 알고리즘 : 최 근접 이웃 알고리즘 즉, KNN
- 하이퍼 파라미터 튜닝 : 모델 성능 개선
"""

# [1] 데이터 준비

import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = '../data/fish.csv'


# 행 : Bream, Smelt, 컬럼 : Species, Weight, Height => 0, 1, 2
fishDF = pd.read_csv(DATA_FILE, usecols = [0, 1, 2])
print(fishDF.head(3))
print()
print()

mask = (fishDF['Species'] == 'Bream') | (fishDF['Species'] == 'Smelt')
twoDF = fishDF[mask]
twoDF.reset_index(drop = True, inplace = True)
print(twoDF.index)
print()
print()

# Species 컬럼을 수치화 => Bream 0, Smelt 1
new_cols = twoDF.loc[:, 'Species'].replace({'Bream' : 0, 'Smelt' : 1})
twoDF['FCode'] = new_cols

print(twoDF.head(3))
print()
print()


# [2] 피쳐와 타겟 분리
features = twoDF[['Weight', 'Length']]
target = twoDF['FCode']

print(f'{features.shape}, {features.ndim}D')
print(f'{target.shape}, {target.ndim}D')
print()
print()

# [3] 데이터셋 준비 => 학습용, 테스트용
from sklearn.model_selection import train_test_split


# train : test = 80:20 ===> test_size = 0.2 또는 train_size = 0.8
# stratify 매개변수 : 분류일 경우 사용, 분류 타겟의 종류에 대한 비율을 고려
X_train, X_test, y_train, y_test = train_test_split(features, 
                                                    target,
                                                    test_size = 0.2,
                                                    stratify = target,
                                                    random_state = 10)

# train : test = 80:20 체크
print(f'X_train : {X_train.shape}, {X_train.ndim}D')
print(f'y_train : {y_train.shape}, {y_train.ndim}D')

print(f'X_test : {X_test.shape}, {X_test.ndim}D')
print(f'y_test : {y_test.shape}, {y_test.ndim}D')

print()
print()

# target 0 (Bream), 1 (Smelt)의 비율
print(y_train.value_counts()[0] / y_train.shape[0], y_train.value_counts()[1] / y_train.shape[0])
print(y_test.value_counts()[0] / y_test.shape[0], y_test.value_counts()[1] / y_test.shape[0])

print()
print()

# [3-2] 피쳐 스케일링 
from sklearn.preprocessing import MinMaxScaler

# 스케일러 인스턴스 생성
mmScaler = MinMaxScaler()

# 데이터에 기반한 MinMaxScaler 동작을 위한 학습 진행
mmScaler.fit(X_train)
print(mmScaler.min_, mmScaler.data_min_, mmScaler.scale_, mmScaler.data_max_)

# 학습용 데이터 셋 ==> 스케일링 ==> ndarray 타입 반환
X_train_scaled = mmScaler.transform(X_train)
print(X_train_scaled.shape)

# 테스트용 데이터셋 ==> 스케일링 => ndarray 타입 반환
X_test_scaled = mmScaler.transform(X_test)
print(X_test_scaled.shape, X_test_scaled.min(), X_test_scaled.max())


# [4] 훈련 / 학습 진행
# - 학습 알고리즘 인스턴스 생성
# - 학습 진행 => fit()

from sklearn.neighbors import KNeighborsClassifier

# 인스턴스 생성
model = KNeighborsClassifier()

# 학습 진행 ==> 학습용 데이터 셋
model.fit(X_train_scaled, y_train)

# 학습 후 모델 파라미터
print(model.classes_, model.n_samples_fit_)
# model.feature_names_in_, <= ndarray일 경우 컬럼명 X



# [5] 모델 성능평가 ==> score() 메서드 + 테스트 데이터 셋
print(f'score : {model.score(X_test_scaled, y_test)}')


# [6] 최적의 K 개수 찾기 ==> 모델의 성능 영향 미치는 파라미터
#   - 하이퍼 파라미터
#   - K의 범위 : 1 ~ 전체 데이터 개수
scores, points = [], []

for k in range(1, 40):
    # 최근접 이웃 데이터 수 설정
    # model = KNeighborsClassifier(n_neighbors = k)
    model.n_neighbors = k
    
    # 모델 예측 값 추출
    # 이미 학습이 되어 있는 상태이기 때문에 k를 바꿀때 마다 fit을 할 필요는 없다
    # model.fit(X_train_scaled)

    # 점수 계산 및 저장
    jumsu = model.score(X_test_scaled, y_test)
#   print(f'[{k}] jumsu => {jumsu}')

    if k > 1:
        if jumsu != scores[-1]: points.append(k)

    scores.append(jumsu)

print(points)

# x 축 k, 축 점수
plt.plot(range(1, 40), scores)
plt.xlabel('K')
plt.ylabel("Scores")
plt.axvline(points[0] - 1, 0.0, 1.0, color = 'red', linestyle = 'dashed')
plt.show()


# [7] 예측 하기 ===> 학습 / 훈련과 테스트에 사용되지 않은 데이터 사용
# - 주의 : 입력 데이터 ==> 2D
new_data = pd.DataFrame([[413, 27.8]], columns = ['Weight', 'Length'])
new_data_scaled = mmScaler.transform(new_data)
print(new_data_scaled)
print()
print()

# 임의의 새로운 데이터의 예측
print(model.predict(new_data_scaled))
print()
print()

distance, index = model.kneighbors(new_data_scaled)

neighbors = index.reshape(-1).tolist()

print(distance)
print(X_train_scaled[neighbors])
print()
print()

k_weight = X_train_scaled[neighbors][:, 0]
k_length = X_train_scaled[neighbors][:, 1]

print(new_data_scaled)
print(k_weight, k_length, sep = '\n')

# 시각화로 확인
# 도미(Bream), 빙어(Smelt)에 대한 시각화 ==> 2개 피쳐 Weight, Length로 Bream, Smelt 분류 가능함
plt.scatter(X_train_scaled[:, 0], X_train_scaled[:, 1])
# plt.scatter(twoDF.loc[35:, 'Weight'], twoDF.loc[35:,'Length'])
plt.plot(new_data_scaled[0, 0], new_data_scaled[0, 1], 'r^')
plt.scatter(k_weight, k_length)
plt.show()
