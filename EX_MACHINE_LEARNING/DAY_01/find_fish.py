"""
생선의 무게와 크기로 생선 분류

- 데이터셋 : fish.csv
- 피쳐 / 입력데이터 : Weight, Length
- 타겟 / 클래스 / 출력 : Species
- 기계 학습 방법 : 지도학습 ==> 분류
- 분류 알고리즘 (문제 해결 방법) : 미정

"""

# [1] 데이터 살펴보기
# [1-1] 데이터 준비

import pandas as pd
import matplotlib.pyplot as plt

# 경로 => 상대 경로, 절대 경로
# 상대 경로 : 현재 파일을 기준으로 경로를 설정
# - ./ : 의미 현재 위치 의미
# -../ : 상위 즉, 한 단계 위의 위치 의미
DATA_FILE = '../Data/fish.csv'

# 절대 경로 : 드라이브 (C, D, E, ...)를 기준으로 경로를 설정
DATA_FILE2 = r'C:\Users\KDP-2\OneDrive\바탕 화면\Python\EX_MACHINE_LEARNING\Data\fish.csv'

# CSV ==> DataFrame으로 읽어오기
# - 첫번째 줄 : 컬럼명
# - 구분자 : 쉼표
# - 로딩 컬럼 : Species, Weight, Length 즉, 0, 1, 2
fishDF = pd.read_csv(DATA_FILE, usecols = [0, 1, 2])
#                                      or ['Species', 'Weight', 'Length']

# [1-1] 데이터 확인
fishDF.info()

# [1-2] 컬럼별 결측치 체크
# -> isnull() X
# -> 컬럼별 고유값 체크 ==> 개수 확인
print(fishDF.value_counts())


# [1-3] 컬럼별 중복값 체크
# => 길이와 무게가 같다고 해서 높이, 너비, 대각선 길이가 같지 않다.
# => 중복 데이터 유지


# [2] 피쳐와 타겟의 관계, 피쳐와 피쳐의 관계
# [2-1] 피쳐와 타겟의 관계 ==> 어느 정도의 연관성이 있는지 확인
# => 상관계수 확인
# => object 타입의 품종을 int로 변환
print(fishDF['Species'].unique())
names = fishDF['Species'].unique().tolist()
print({ name : idx + 1 for idx, name in enumerate(names) }) # 딕셔너리 컨프리헨션 dict comprehension

values = {'Bream' : 1, 'Roach' : 2, 'Whitefish' : 3, 'Parkki' : 4, 'Perch' : 5, 'Pike' : 6, 'Smelt' : 7}
fishDF['Num'] = fishDF['Species'].replace(values)
print(fishDF.head())

# 7가지 종류에 대한 상관계수
print(fishDF.corr(numeric_only = True))
print()
print()

# 도미(Bream), 빙어(Smelt)에 대한 상관계수
mask = (fishDF["Species"] == "Bream") | (fishDF['Species'] == 'Smelt')
twofishDF = fishDF[mask]
print(twofishDF.corr(numeric_only = True))


# 도미(Bream), 빙어(Smelt)에 대한 시각화 ==> 2개 피쳐 Weight, Length로 Bream, Smelt 분류 가능함
plt.scatter(twofishDF.loc[:34, 'Weight'], twofishDF.loc[:34, 'Length'])
plt.scatter(twofishDF.loc[145:, 'Weight'], twofishDF.loc[145:,'Length'])
plt.show()

print()
print()


# [3] 학습 훈련 진행
#   - 지도 학습 ==> 분류
#   - ML프레임워크 ==> Scikit-learn
#   - 학습 알고리즘 ==> 최 근접 이웃 알고리즘 즉, KNN

# 모듈 로딩
from sklearn.neighbors import KNeighborsClassifier


# [1] 학습 인스턴스 생성 ==> 클래스 명(매개 변수 값)
model = KNeighborsClassifier()

print(model, model.n_neighbors) # ERROR, model.classes_)
print()
print()

# [2] 학습 / 훈련 진행
# model.fit(피쳐2D, 타겟1D)
features = twofishDF[['Weight', 'Length']]
target = twofishDF['Num']

print(f'features.shape :  {features.shape}, {features.ndim}D')
print(f'target.shape :  {target.shape}, {target.ndim}D')
print()
print()

model.fit(features, target)


# 모델 파라미터(Model Parameter) : 학습 후 설정되는 속성
# - 파라미터 이름 : XXX_ 
print(model.classes_, model.feature_names_in_)
print()
print()

# [4] 검증 
#   - KNN은 모델 즉 규칙 및 패턴이 생성 X
#   - 검증 데이터가 입력이 되면 학습 데이터와 거리 측정
#   - 지정된 k 개수 만큼 검증 데이터와 가까운 데이터를 도출
#   - 분류일 경우 K 개수 데이터가 가진 라벨/타겟/클래스에 따라 다수결로 결정

print(twofishDF.head())
print()
print()

# 검증 데이터와 타겟
data = twofishDF.loc[:4, ['Weight', 'Length']]
target = twofishDF.loc[:4, 'Num']
print(data.shape, data.ndim, target.shape, target.ndim)
print()
print()

# 새로운 데이터에 대해서 결과를 예측
# - model.predict(2D) ==> 1D
pre_target = model.predict(data)
print(pre_target)

# 예측 결과와 정답을 비교해서 점수를 도출
# - model.score(2D 피쳐, 1D 타겟)
# - 결과 : 0.0 ~ 1.0
print(model.score(data, target))