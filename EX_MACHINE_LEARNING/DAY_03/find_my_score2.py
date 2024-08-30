"""
공부 시간과 과외 횟수에 따른 점수 예측하기
- 목표 : 공부 시간과 과외 횟수가 가지는 패턴 / 규친을 찾아서 점수를 예측
- 데이터셋 : 임의의 생성
- 피쳐 / 속성 : 공부 시간, 과외 횟수
- 타겟 / 라벨 : 점수
- 학습 방법 : 지도 학습 > 회귀
- 알고리즘 : 선형 회귀 <== [조건] : 데이터 분포가 선형 분포여야 함!
"""

import pandas as pd
import matplotlib.pyplot as plt

# [1] 데이터 준비
hour = [1, 3, 4, 5, 7, 9, 10]
jumsu = [32, 55, 83, 70, 99, 92, 100]
lesson = [0, 0, 2, 1, 2, 0, 1]

# 현재 데이터의 분포 확인
plt.plot(hour, jumsu, 'go')
plt.xlabel('Hour')
plt.ylabel('Jumsu')
plt.show()

# 학습용 데이터셋 구성 => 피쳐와 타겟
dataDF = pd.DataFrame({"Hour" : hour, 'Lesson' : lesson})
jumsuSR = pd.Series(jumsu)

# [2] 학습 진행 - 다중 선형 회귀
# 모듈 로딩
from sklearn.linear_model import LinearRegression

# 학습 모델 인스턴스 생성
model = LinearRegression()

# 학습 진행 => coef_, intercept_ 구할 수 있음
model.fit(dataDF, jumsuSR)

print(f"model.coef_ : {len(model.coef_)}개, {model.coef_}")
print(f"model.intercept_ : {model.intercept_}\n\n")

# 점수 => 내부에서 predict()진행 ===> 결과로 R2 계수 추출해서 반환
score = model.score(dataDF, jumsuSR)
print(f"score : {score}\n\n")


# 오차 계산 즉, 손실/비용 함수 확인
# - root_mean_squared_error sklearn v1.4 이상
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# 성능 지표 => 오차 계산과 결정 계수 계산
pre_jumsu = model.predict(dataDF)


# 손실/비용 계산 함수 ==> 정답과 예측값 : 0에 가까울 수록 좋음
mse = mean_squared_error(jumsuSR, pre_jumsu)
rmse = mean_squared_error(jumsuSR, pre_jumsu, squared = False)
mae = mean_absolute_error(jumsuSR, pre_jumsu)

# 얼마나 정답에 가깝게 값을 예측 했느냐를 나타내는 지표 ==> 정답과 예측값 제공 : 1에 가까울 수록 좋음
r2 = r2_score(jumsuSR, pre_jumsu)


# 손실/비용 함수 값은 0에 가까울수록
# 결정계수 값은 1에 가까울수록 성능 좋은 모델 
print(f"mse : {mse}")
print(f"rmse : {rmse}")
print(f"mae : {mae}")
print(f"r2 : {r2}")