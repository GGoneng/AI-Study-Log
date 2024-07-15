"""
모듈 - 파이썬 파일(py) 1개
- 구성 : 변수, 함수, 클래스가 존재
         반드시 모두 다 있지는 않음!
- 종류 : 내장 모듈 / 사용자 정의 모듈 / 써드 파티션 모듈 (설치 필수)
"""

# 사용법 => 현재 파이썬 파일에 포함시켜야 사용 가능함
import math
# 모듈명이 길 경우 줄여서 별칭 지정 후 사용
import random as rad

# 모듈 내의 변수, 함수, 클래스 사용 방법
# : 모듈명.변수명,  모듈명.함수(),  모듈명.클래스명
print(f"내장 모듈 math 안에 있는 pi변수 : {math.pi}")

print(F"내장 모듈 math 안에 있는 factorial() 함수 : {math.factorial(3)}")

print(F"내장 모듈 random 안에 있는 random() 함수 : {rad.random()}")
# 모듈명을 별칭 지정 시 이전 모듈명으로 사용 X
# random.randint()