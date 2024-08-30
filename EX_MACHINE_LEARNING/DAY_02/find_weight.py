"""
무게를 찾기
- 목표 : 농어 (Perch) 길이 피쳐를 사용해서 무게를 예측하기
- 데이터셋 : fish.csv
- 피쳐 / 속성 : Length
- 타겟 / 라벨 : Weight
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import koreanize_matplotlib

# [1] 데이터 준비 및 피쳐 / 타겟 분석
DATA_FILE = "../Data/fish.csv"
fishDF = pd.read_csv(DATA_FILE)
print(f"fish DataFrame :\n{fishDF}\n\n")

# 농어 데이터만 뽑기
fishDF = fishDF[fishDF["Species"] == "Perch"].reset_index()[["Species", "Length", "Weight"]]
fishDF["Code"] = fishDF["Species"].replace({"Perch" : 0})
print(f"Perch DataFrame :\n{fishDF}\n\n")


# [2] 학습 준비
#   - 학습 알고리즘 : KNN Regressor
#   - 피쳐 스케일링
#   - 학습용 / 테스트용 데이터 셋 분리

features = fishDF[["Length"]]
target = fishDF["Weight"]

print(f"features : {features.shape}, {features.ndim}D \n\n")
print(f"target : {target.shape}, {target.ndim}D \n\n")



plt.scatter(features, target, label = "Perch")
plt.title("농어의 길이와 무게의 상관관계")
plt.legend()
plt.show()


# [2-2] 학습용 & 테스트용 데이터 셋 분리
#   전체 데이터 셋 => 학습용 : 테스트용 = 75:25, 80:20, 70:30
#   회귀 데이터 셋 => 데이터 셋 구성 요소에 대한 비율 고려 X
X_train, X_test, y_train, y_test = train_test_split(features,
                                                    target,
                                                    test_size = 0.2,
                                                    random_state = 10)
 

X_train = X_train.reset_index(drop = True)
y_train = y_train.reset_index(drop = True)

X_test = X_test.reset_index(drop = True)
y_test = y_test.reset_index(drop = True)



# [2-3] 피쳐 스케일링
from sklearn.preprocessing import MinMaxScaler

# 스케일러 인스턴스 생성
mmScaler = MinMaxScaler()

# 스케일러에 데이터 셋 전용의 속성값 설정
mmScaler.fit(X_train)

print(mmScaler.min_, mmScaler.scale_, mmScaler.data_min_, mmScaler.data_max_)


# 학습용, 테스트용 데이터 셋 스케일링 진행
X_train_scaled = mmScaler.transform(X_train)
X_test_scaled = mmScaler.transform(X_test)


# [3] 학습 진행

X = [[0], [1], [2], [3]]
y = [0, 0, 1, 1]

from sklearn.neighbors import KNeighborsRegressor

neigh = KNeighborsRegressor(n_neighbors = 2)
neigh.fit(X, y)

print(neigh.predict([[3]]))

distance, index = neigh.kneighbors([[3]])
print(distance, index)

index = index.reshape(-1)

for idx in index.tolist():
    print(idx, y[idx])

plt.scatter([0, 1, 2, 3], [0, 0, 1, 1])
plt.plot()
plt.show()

model = KNeighborsRegressor()
model.fit(X_train_scaled, y_train)

# 모델 파라미터 => 학습 후 즉, fit() 실행 후 설정되는 매개변수
print(model.n_features_in_, model.n_samples_fit_, model.effective_metric_, model.effective_metric_params_ )


scores = {}
for k in range(1, model.n_samples_fit_ + 1):
    # 최근접 이웃의 갯수 설정 <== 모델 성능 좌우 : 하이퍼 파라미터
    model.n_neighbors = k

    # 성능 평가
    score = (model.score(X_test_scaled, y_test))
    scores[k] = score


list(scores.values())

plt.plot(list(scores.keys()), list(scores.values()))
plt.grid()
plt.show()

# 최고 성능의 K값
best_k = sorted(scores.items(), key = lambda x: x[1], reverse = True)[0][0]
print(best_k, "\n\n")

# 모델에 적용 => n_neighbors에 설정
model.n_neighbors = best_k


# [5] 새로운 데이터의 무게 예측하기
new_length = input("농어 길이 : ")
print(f"new_length : {new_length}\n\n")

# 2D DataFrame
dataDF = pd.DataFrame([[new_length]], columns = ["Length"])
print(dataDF, "\n\n")

# 피쳐 스케일링
data_scaled = mmScaler.transform(dataDF)
print(data_scaled, "\n\n")


# 예측
print(model.predict(data_scaled))


distance, index = model.kneighbors(data_scaled)

print(distance, index, sep = "\n")

print(X_train.iloc[index.reshape(-1)])
print(X_train_scaled[[33, 29, 5, 32, 17, 9]])



print(y_train[index.reshape(-1)].sum() / model.n_neighbors)


# KNN Regressor 문제점 / 단점

# 임의의 데이터
new_length = 4

# 2D DataFrame
dataDF = pd.DataFrame([[new_length]], columns = ['Length'])
# 피쳐 스케일링
data_scaled = mmScaler.transform(dataDF)

# 예측
print(model.predict(data_scaled))


# => 학습 데이터셋의 범위를 벗어난 더 큰 데이터, 더 작은 데이터의 경우
#    정확한 예측 불가!!