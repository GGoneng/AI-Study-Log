"""
무게를 찾기
- 목표 : 농어 (Perch) 길이 피쳐를 사용해서 무게를 예측하기
- 데이터 셋 : fish.csv
- 피쳐/속성 : Length
- 타겟/라벨 : Weight
- 학습 방법 : 지도학습 > 회귀
- 알고리즘 : 선형회귀 >>> 데이터 분포가 선형의 형태
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
import numpy as np


DATA_FILE = "../Data/fish.csv"
fishDF = pd.read_csv(DATA_FILE)
print(f"fish data : \n {fishDF}\n\n")

fishDF = fishDF[fishDF["Species"] == "Perch"]
fishDF.reset_index(inplace = True)
fishDF = fishDF[["Length", "Weight"]]


print(f"fishDF's Null : \n {fishDF.isnull().sum()}\n")
print(f"fish data : \n{fishDF}\n\n")
print(f"{fishDF.info()}\n\n")

print(f"fish data's correlation : \n{fishDF.corr()}\n\n")

plt.boxplot(fishDF)
plt.show()

plt.scatter(x = range(len(fishDF)), y = fishDF["Length"])
plt.show()


features = fishDF[["Length"]]
target = fishDF["Weight"]


X_train, X_test, y_train, y_test = train_test_split(features, 
                                                    target,
                                                    test_size = 0.2,
                                                    random_state = 10)


# mmScaler = MinMaxScaler()

# mmScaler.fit(X_train)

# X_train_scaled = mmScaler.transform(X_train)
# X_test_scaled = mmScaler.transform(X_test)

# print(f"Scaled X_train : \n{X_train_scaled}\n\n")
# print(f"Scaled X_test : \n{X_test_scaled}\n\n")

model = LinearRegression()

model.fit(X_train, y_train)

print(f"model.coef_ : {len(model.coef_)}개, {model.coef_}")
print(f"model.intercept_ : {model.intercept_}\n\n")

print(f"model's score : \n{model.score(X_test, y_test)}\n\n")
print(f"model's score : \n{model.score(X_train, y_train)}\n\n")
print(f"model's prediction : \n{model.predict(X_test)}")

predict_value = model.predict(X_test)

plt.plot(X_train, y_train, 'bo')
plt.plot([10, 50], [10 * model.coef_ + model.intercept_, 50 * model.coef_ + model.intercept_])
plt.show()

plt.plot(X_test, y_test, 'bo')
plt.plot(X_test, predict_value, 'ro')
plt.vlines(X_test, y_test, predict_value)
plt.show()

print(target)

def true_fun(X):
    return np.cos(1.5 * np.pi * X)

plt.figure(figsize = (14, 10))

degrees = [1, 4, 5]







# for i in range(len(degrees)):
#     ax = plt.subplot(1, len(degrees), i + 1)
#     plt.setp(ax, xticks = (), yticks = ())
    
#     polynomial_features = PolynomialFeatures(degree = degrees[i], include_bias = False)
#     linear_regression = LinearRegression()
#     pipeline = Pipeline([("polynomial_features", polynomial_features),
#                          ("linear_regression", linear_regression)])
    
#     pipeline.fit(np.array(features["Length"]).reshape(-1, 1), np.array(target))

#     scores = cross_val_score(pipeline, np.array(features["Length"]).reshape(-1, 1), np.array(target).reshape(-1, 1), scoring = "neg_mean_squared_error", cv = 10)
#     coefficients = pipeline.named_steps['linear_regression'].coef_
#     print("\nDegree {0} 회귀 계수는 {1} 입니다.".format(degrees[i], np.round(coefficients, 2)))
#     print("Degree {0} MSE는 {1} 입니다.".format(degrees[i], -1 * np.mean(scores)))
    
#     X_test = np.linspace(0, 1, 100)

#     plt.plot(X_test, pipeline.predict(X_test[:, np.newaxis]), label = "Model")
#     plt.plot(X_test, true_fun(X_test), '--', label = "True function")
#     plt.scatter(features, target, edgecolor = 'b', s = 20, label = "Samples")

#     plt.xlabel("x"); plt.ylabel("y"); plt.xlim((0, 1)); plt.ylim((-2, 2)); plt.legend(loc = "best")
#     plt.title("Degree {}\nMSE = {:.2e}(+/- {:.2e})".format(degrees[i], -scores.mean(), scores.std()))

# plt.show()