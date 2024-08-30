from sklearn.datasets import load_diabetes
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

# 데이터 불러오기
dataDict = load_diabetes(as_frame = True, scaled = False)
print(dataDict.keys(), "\n\n")

data = dataDict["data"]
target = dataDict["target"]



print(data.info(), "\n\n")
print(target.info(), "\n\n")

# 이상치 제거는 하지 않음
plt.boxplot(data)
plt.legend()
plt.show()

# 데이터와 타겟 합치기
data["target"] = target

print(data)

# features를 찾기 위한 연관 분석
print(data.corr(), "\n\n")
# 연관이 높은 features 후보 : bmi, s5, bp, s4


# 산점도는 의미 없어 보임
# plt.scatter(data["target"], data["bmi"])
# plt.scatter(data["target"], data["s5"])
# plt.show()

features = data[["bmi", "s5"]]
target = data["target"]

print(features, target, sep = '\n')

print(f"features : {features.shape}, {features.ndim}D ")
print(f"target : {target.shape}, {target.ndim}D \n\n")


X_train, X_test, y_train, y_test = train_test_split(features,
                                                    target,
                                                    test_size = 0.2,
                                                    random_state = 10)

# 피쳐 스케일링
mmScaler = MinMaxScaler()

mmScaler.fit(X_train)
print(f"mmScaler's min_ : {mmScaler.min_}")
print(f"mmScaler's scale_ : {mmScaler.scale_}")
print(f"mmScaler's data_min_ : {mmScaler.data_min_}")
print(f"mmScaler's data_max_ : {mmScaler.data_max_}\n\n")

X_train_scaled = mmScaler.transform(X_train)
X_test_scaled = mmScaler.transform(X_test)

# print(X_train_scaled)
# print()
# print(X_test_scaled)

model = KNeighborsRegressor()

model.fit(X_train_scaled, y_train)

print(f"model's n_features_in_ : {model.n_features_in_}")
print(F"model's n_samples_fit_ : {model.n_samples_fit_}")
print(f"model's effective_metric_ : {model.effective_metric_}")
print(f"model's effective_metric_params : {model.effective_metric_params_}\n\n")

# 최적의 K 찾기
scores = {}
for k in range(1, model.n_samples_fit_ + 1):
    model.n_neighbors = k

    score = (model.score(X_test_scaled, y_test))
    scores[k] = score

plt.plot(list(scores.keys()), list(scores.values()))
plt.grid()
plt.show()

print(f"sorted by scores :\n{sorted(scores.items(), key = lambda x: x[1], reverse = True)}\n\n")
best_k = sorted(scores.items(), key = lambda x: x[1], reverse = True)[0][0]
print(f"best_k : {best_k}\n\n")

model.n_neighbors = best_k

# 모델 예측
new_data = pd.DataFrame([[0, 0]], columns = ['bmi', 's5'])
new_data_scaled = mmScaler.transform(new_data)

print(f"New data prediction : \n{model.predict(new_data_scaled)}\n\n")

distance, index = model.kneighbors(new_data_scaled)
neighbors = index.reshape(-1).tolist()

print(f"neighbors : \n{X_train_scaled[neighbors]}\n\n")

k_bmi = X_train_scaled[neighbors][:, 0]
k_b5 = X_train_scaled[neighbors][:, 1]

print(k_bmi, k_b5, sep = "\n")
print()

# print(f"X_train_scaled : \n{X_train_scaled}\n\n")
# print(f"new_data_scaled : \n{new_data_scaled}\n\n")


plt.scatter(X_train_scaled[:, 0], X_train_scaled[:, 1], label = "X_train_data")
plt.plot(new_data_scaled[0, 0], new_data_scaled[0, 1], 'r^', label = "new_data_scaled")
plt.scatter(k_bmi, k_b5, label = "neighbors")
plt.title("bmi & b5's Scatter with neighbors")
plt.xlabel("bmi")
plt.ylabel("b5")
plt.legend()
plt.show()
