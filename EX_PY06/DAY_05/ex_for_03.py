"""
제어문 - 반복문
"""

# [실습] 출력하고 싶은 단을 입력 받아서
#        해당 단의 구구단을 출력하세요.
# [출력 예시] 2 * 1 = 2...

num = int(input("숫자를 입력하세요 : "))

for i in range(1, 10):
    print(f"{num} * {i} = {num * i}")

print()

# enumerate() 사용
result = [num * i for i in range(1, 10)]
for e in enumerate(result):
    print(F"{num} * {e[0] + 1} = {e[1]}")