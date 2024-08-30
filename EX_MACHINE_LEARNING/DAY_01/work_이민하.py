"""
iris 데이터 셋 품종 구별
101열 까지의 데이터 사용 (두 개의 품종)
"""

# [1] 모듈 삽입

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import koreanize_matplotlib


# [2] 데이터 셋 준비

DATA_FILE = "../Data/iris.csv"
irisDF = pd.read_csv(DATA_FILE)
print(f"Iris data's head : \n{irisDF.head()}\n\n")
print(f"Iris data's info : \n{irisDF.info()}\n\n")

# [3] 데이터 전처리
#   - 결측치, 중복치, 이상치 검사   

print(f"Numbers of Null : \n{irisDF.isna().sum()}\n\n")
print(f"Numbers of Duplication : \n{irisDF.duplicated().sum()}\n\n")

colors = ['peachpuff', 'orange', 'tomato', 'blue']
bplot = plt.boxplot([irisDF['sepal.length'], irisDF['sepal.width'], irisDF['petal.length'], irisDF['petal.width']],
            patch_artist = True)
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)
plt.title("Iris 데이터의 박스 플롯")
plt.show()

# 중복치와 이상치의 경우, 데이터의 표본 수도 적고, 충분히 중복이나 이상치가 아니라고 판단되어 제거 X

# [3-1] 데이터 자르기
irisDF = irisDF.iloc[:100]
print(f"iris DataFrame (100 rows) : \n{irisDF}\n\n")

# [3-2] 종류 (범주화 데이터) ==> 코드 (수치화 데이터)로 전환
new_cols = {'Setosa' : 0, 'Versicolor' : 1}
irisDF['Vcode'] = irisDF['variety'].replace(new_cols)
print(f"new irisDF : \n{irisDF}\n\n")

# [3-3] features 선정 => 상관관계 체크
print("iris DataFrame's Correlation :")
print(f"{irisDF.corr(numeric_only = True)}\n\n")

# [3-4] 사용할 열 고르기 (petal.length, petal.width, variety)
irisDF = irisDF[['petal.length', 'petal.width', 'Vcode']]
print(f"iris DataFrame (3 columns) : \n{irisDF}\n\n")

# [4] 피쳐와 타겟 분리
# - features => petal.length, petal.width
# - target => variety
features = irisDF[['petal.length', 'petal.width']]
target = irisDF['Vcode']

# features는 무조건 2차원, 타겟은 1차원
print("features and target's shape and dimension :")
print(f"features' shape : {features.shape}, features' dimension : {features.ndim}D")
print(f"target's shape : {target.shape}, target's dimension : {target.ndim}D")


# [5] 데이터셋 준비 => 학습용, 테스트용
X_train, X_test, y_train, y_test = train_test_split(features,
                                                    target,
                                                    test_size = 0.2,
                                                    stratify = target,
                                                    random_state = 10)

# train : test = 80 : 20 체크
print('\n\ntrain and test rate:')
print(f"X_train's shape : {X_train.shape}, X_train's dimension : {X_train.ndim}D")
print(f"y_train's shape : {y_train.shape}, y_train's diemnsion : {y_train.ndim}D")
print()
print(f"X_test's shape : {X_test.shape}, X_test's dimension : {X_test.ndim}D")
print(f"y_test's shape : {y_test.shape}, y_test's dimension : {y_test.ndim}D")


# [6] 훈련 및 학습 진행
model = KNeighborsClassifier()

model.fit(X_train, y_train)

print("\n\nCheck model :")
print(model.classes_, model.feature_names_in_, model.n_samples_fit_)

print("\n\nModel Score :")
print(model.score(X_test, y_test))


# [7] 예측 하기 (2D)
new_data = pd.DataFrame([[4.0, 1.5]], columns = ['petal.length', 'petal.width'])
print(f"\n\nnew data : \n{new_data}\n\n")
print(f"Predict result : \n{model.predict(new_data)}\n\n")


# [8] 산점도로 살펴보기
distance, index = model.kneighbors(new_data)
neighbors = index.reshape(-1).tolist()
print(f"neighbors' index : \n{neighbors}\n\n")
print(f"distance : \n{distance}\n\n")
print(f"neighbors : \n{X_train.iloc[neighbors]}\n\n")

petal_length = X_train.iloc[neighbors]['petal.length'].values
petal_width = X_train.iloc[neighbors]['petal.width'].values

print(f"new_data :\n{new_data}\n")
print("neighbors' length and width")
print(petal_length, petal_width, sep = "\n")

plt.scatter(X_train['petal.length'], X_train['petal.width'])
plt.scatter(petal_length, petal_width)
plt.plot(new_data['petal.length'], new_data['petal.width'], 'r^')
plt.show()