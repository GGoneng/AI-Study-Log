"""
제어문 - while 반복문
"""

# [실습] 3단 출력하기. 단, while문 사용

num = 1
dan = 3

while num < 10:
    print(F"{dan} * {num} = {dan * num}")
    num += 1

# [실습] 1 ~ 30 범위의 수 중에서 홀수만 출력
#       단 while문 사용
# [1] 1 ~ 30 숫자 while문으로 출력
num = 1
while num <= 30:
    print(num)
    num += 1

# [2] 홀수만 출력
num = 1
while num < 31:
    if num % 2 == 0:
        print(num)
    num += 1

num = 1
while num < 31:
    print(num)
    num += 2
    