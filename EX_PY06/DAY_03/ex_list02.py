"""
List 데이터 자료형 살펴보기
- 원소 / 요소 변경하기 -> 데이터 변경, 삭제
"""

datas = [1, 3, 5, 7, 9, 11]

# 0번 원소를 100으로 변경하기
datas[0] = 100
print(datas)

# 0번 원소를 삭제하기
del datas[0]
print(datas)

# datas = [3, 5, 7, 9, 11]
# 0번 ~ 2번 원소까지 자리에 삼 오 칠 변경

datas[:3] = ["삼", "오", "칠"]
print(datas)

# 0번 ~ 2번 원소 자리에 100으로 변경
datas[:3] = [100, 100, 100]
print(datas)

# 0번 ~ 2번 원소 자리에 22, 33, 44, 55, 66, 77, 88
datas[:2] = [22, 33, 44, 55, 66, 77, 88]
print(datas)


datas[:] = []
print(datas)

# 여러 개 원소를 삭제하기
datas = [22, 33, 44, 55, 66, 77, 88, 11]
del datas[0:3]
print(datas)