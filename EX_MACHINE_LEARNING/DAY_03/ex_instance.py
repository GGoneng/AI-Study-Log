"""
클래스와 인스턴스
"""

# 임시 데이터 생성
import random

data = []

random.seed(10)

for _ in range(30):
    data.append([random.randint(1, 50)])

# 스케일러에서 fit()시에 진행
print(min(data), max(data))

# 스케일러에서 transform()시에 0 ~ 1 사이 값으로 전부 변환
result = [d[0] / max(data)[0] for d in data]

print(min(result), max(result))