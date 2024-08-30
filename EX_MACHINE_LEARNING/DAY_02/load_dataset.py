from sklearn.datasets import load_diabetes
import pandas as pd
import matplotlib.pyplot as plt

# 기본 : ndarray 형태로 반환
# 반환값 : Bunch 객체로 dict와 유사

dataDict = load_diabetes()
print(dataDict.keys())


# 기본 : DataFrame 형태로 반환
# 반환값 : Bunch 객체로 dict와 유사

dataDict = load_diabetes(as_frame = True)
print(dataDict.keys())


# 기본 : ndarray 형태로 반환
# 반환값 : tuple로 data와 target만 반환

data, target = load_diabetes(return_X_y = True)
print(dataDict.keys())


# 기본 : DataFrame 형태로 반환
# 반환값 : tuple로 data와 target만 반환

data, target = load_diabetes(return_X_y = True, as_frame = True)
print(dataDict.keys())


dataDF = dataDict['data']
targetST = dataDict['target']

print(targetST.head())