"""

생선 분류
- 데이터셋 : fish.csv
- 피쳐 / 특성 : Weight, Length
- 타겟 / 라벨 : Species
- 학습 방법 : 지도 학습 => 분류
- 학습 알고리즘 : 최 근접 이웃 알고리즘 즉, KNN

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


# [4] 훈련 / 학습 진행
# - 학습 알고리즘 인스턴스 생성
# - 학습 진행 => fit()

from sklearn.neighbors import KNeighborsClassifier

# 인스턴스 생성
model = KNeighborsClassifier()

# 학습 진행 ==> 학습용 데이터 셋
model.fit(X_train, y_train)

# 학습 후 모델 파라미터
print(model.classes_, model.feature_names_in_, model.n_samples_fit_)


# [5] 모델 성능평가 ==> score() 메서드 + 테스트 데이터 셋
print(f'score : {model.score(X_test, y_test)}')


# [6] 예측 하기 ===> 학습 / 훈련과 테스트에 사용되지 않은 데이터 사용
# - 주의 : 입력 데이터 ==> 2D
new_data = pd.DataFrame([[413, 27.8]], columns = model.feature_names_in_)

print(model.predict(new_data))
print()
print()

distance, index = model.kneighbors(new_data)

neighbors = index.reshape(-1).tolist()

print(distance)
print(twoDF.iloc[neighbors])


# 시각화로 확인
# 도미(Bream), 빙어(Smelt)에 대한 시각화 ==> 2개 피쳐 Weight, Length로 Bream, Smelt 분류 가능함
plt.scatter(twoDF.loc[:34, 'Weight'], twoDF.loc[:34, 'Length'])
plt.scatter(twoDF.loc[35:, 'Weight'], twoDF.loc[35:,'Length'])
plt.plot(new_data['Weight'], new_data['Length'], 'r^')
plt.scatter(twoDF.iloc[neighbors]["Weight"], twoDF.iloc[neighbors]['Length'])
plt.show()
