"""
피쳐 전처리
- 수치형 피쳐 전처리 ==> 스케일링
- 범주형 피쳐 전처리 ==> 인코딩
"""

# 모듈 로딩
from sklearn.preprocessing import LabelEncoder

items = ['TV', '냉장고', '선풍기', '에어컨']

# 라벨 / 정수 인코더 인스턴스 생성
lencoder = LabelEncoder()


# 라벨 / 정수 인코더의 범위 및 맵핑 작업
lencoder.fit(items)

# 라벨 / 정수 값으로 변환
print(lencoder.transform(items), "\n\n")


# One-Hot-Encoder 원-핫-인코더
from sklearn.preprocessing import OneHotEncoder
import numpy as np

# 인코더 인스턴스 생성
ohEncoder = OneHotEncoder()

# 원핫 인코더의 범위 및 맵핑 작업
arr_items = np.array(items).reshape(-1, 1)
print(arr_items.shape, "\n\n")
ohEncoder.fit(arr_items)

oh_items = ohEncoder.transform(arr_items)
print(type(oh_items), "\n\n")

print(oh_items.toarray(), "\n\n")


# 정수 인코딩 ==> 범주형 피쳐
from sklearn.preprocessing import OrdinalEncoder

data = [['male', 'C', 'child'], ['female', 'S', 'child']]

# 정수 인코더 인스턴스 생성
odEncoder = OrdinalEncoder()

# 정수 인코딩 범위 및 맵핑 진행
odEncoder.fit(data) # fit(2D)

# 범주 피쳐 => 정수 피쳐 변환
print(odEncoder.transform(data), "\n\n")
