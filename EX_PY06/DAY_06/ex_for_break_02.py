"""
제어문 - 반복문과 break
- 중첩 반복문일 경우의 break는 가장 가까이 있는 반복문만 종료
"""

# [실습] 단의 숫자만큼만 구구단 출력하세요.
# 2 * 1 = 2  2 * 2 = 4
# 3 * 1 = 3  3 * 2 = 6  3 * 3 = 9
# 4 * 1 = 4  4 * 2 = 8  4 * 3 = 12  4 * 4 = 16

# [중첩 반복문] 내부 반복문 종료 시 외부 반복문 종료

# dan = int(input("출력 원하는 단 입력 : "))
isBreak = False

for d in range(2, 10):
    print(f"\n[{d}단]", end = "\t")
    for n in range(1, 10):
        print(F"{d} * {n} = {d * n :<2}", end = "\t")
        if n == d: 
            isBreak = True
            break
    if isBreak: break

