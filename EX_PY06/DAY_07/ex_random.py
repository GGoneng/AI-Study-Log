"""
모듈 : 변수, 함수, 클래스가 들어있는 파이썬 파일
패키지 : 동일한 목적의 모듈들을 모은 것
        여러 개의 모듈 파일들 존재
모듈 사용법 : import 모듈 파일명  <-- 확장자 제외
"""

import random as rad

# 임의의 숫자를 생성 추출하기
# 임의의 숫자 10개 생성
# -> random() : 0.0 <= ~ < 1.0
for i in range(10):
    print(int(rad.random() * 10))

# -> randint(a, b) : a <= ~ <= b
for cnt in range(10):
    print(rad.randint(0, 1))


# [실습] 로또 프로그램을 만들어주세요.
# - 1 ~ 45 범위에서 중복되지 않는 6개 추출

# L = []

# while True:
#     if len(L) >= 6:
#         break
#     num = rad.randint(1, 45)
#     if num not in L:
#         L.append(num)   
# print(L)

# lotto = [0, 0, 0, 0, 0, 0]
# idx = 0
# while True:
#     num = rad.randint(1, 45)
#     if num not in lotto:
#         lotto[idx] = num
#         idx += 1
#     if idx == 6 : break
# print(lotto)

lotto = dict()
idx = 0

while True:
    if len(lotto) >= 6:
        break
    num = rad.randint(1, 45)
    if num not in lotto.values():
        lotto[idx] = num
        idx += 1
print(lotto.values())


# set 타입의 add() 메서드
lotto = set()
while len(lotto) < 6:
    num = rad.randint(1, 45)
    lotto.add(num)
print(lotto)