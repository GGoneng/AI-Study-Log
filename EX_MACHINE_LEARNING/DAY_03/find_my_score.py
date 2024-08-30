"""
공부 시간에 따른 점수 예측하기
- 목표 : 공부 시간으로 점수를 예측
- 데이터셋 : 임의의 생성
- 피쳐 / 속성 : 공부 시간
- 타겟 / 라벨 : 점수
- 학습 방법 : 지도 학습 > 회귀
- 알고리즘 : 선형 회귀 <== [조건] : 데이터 분포가 선형 분포여야 함!
"""

import pandas as pd
import matplotlib.pyplot as plt

# [1] 데이터 준비
jumsu = range(7, 100, 7)
print(len(jumsu), jumsu[-1])

hour = list(range(1, 29, 2))
print(len(hour), hour[-1])


# List => DataFrame으로 변환
hourDF = pd.DataFrame(hour, columns = ['hour'])
print(hourDF.head(), "\n\n")

jumsuSR = pd.Series(jumsu)
print(jumsuSR.head(), "\n\n") 

plt.plot(hourDF, jumsuSR, 'go')
plt.xlabel('Hour')
plt.ylabel('Jumsu')
plt.show()

# [2] 모델 생성 및 학습 진행
# 모듈 로딩
from sklearn.linear_model import LinearRegression

# 학습 모델 인스턴스 생성
model = LinearRegression()

# 학습 진행 => 최대한 많은 데이터를 만족하는 직선의 기울기와 절편 찾기
model.fit(hourDF, jumsuSR)

print(f"기울기 : {model.coef_}, 절편 : {model.intercept_}\n")

# y = ax + b
pre_jumsu = model.coef_[0] * hourDF + model.intercept_
pre_jumsu = pre_jumsu.values.reshape(-1)



# 실제 점수와 예측 점수의 차이 확인
print(pre_jumsu.shape, "\n\n")

real_jumsu = jumsuSR.to_numpy()
print(real_jumsu - pre_jumsu)

plt.plot(hourDF, jumsuSR, 'go', label = 'Real Jumsu')
plt.plot(hourDF, pre_jumsu, 'r^', label = 'Predict Jumsu')
plt.xlabel('Hour')
plt.ylabel('Jumsu')
plt.legend()
plt.show()

print(model.score(hourDF, jumsuSR))

# 오차 계산 즉, 손실/비용 함수 확인
# - root_mean_squared_error sklearn v1.4 이상
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

pre_y = model.predict(hourDF)

mse = mean_squared_error(jumsuSR, pre_y)
rmse = mean_squared_error(jumsuSR, pre_y, squared = False)
mae = mean_absolute_error(jumsuSR, pre_y)
r2 = r2_score(jumsuSR, pre_y)


# 손실/비용 함수 값은 0에 가까울수록
# 결정계수 값은 1에 가까울수록 성능 좋은 모델 
print(f"mse : {mse}")
print(f"rmse : {rmse}")
print(f"mae : {mae}")
print(f"r2 : {r2}")