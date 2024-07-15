"""
제어문 - 반복문과 조건문 혼합
"""

# [실습]
# 숫자 1 ~ 50까지의 데이터가 있습니다.
# 해당 데이터에서 3의 배수는 제곱을 하고, 
# 나머지 숫자는 그대로 해서 모두 더해서 합계를 출력하세요.

# datas = list(range(1, 51))

# for data in datas:
#     if data % 3 == 0:
#         datas[data - 1] = data ** 2

# print(sum(datas))

datas = range(1, 51)
total = 0

for data in datas:
    # 3의 배수 여부 검사
    if data % 3:
        total = total + data
    else:
        total = total + (data * data)

print(total)

# [실습]
# 메시지에서 알파벳과 숫자를 구분해서 처리합니다.
# 알파벳은 ★, 숫자는 ♡로 변경해서 출력해주세요.

msg = "Good 2024"
msg2 = ""

for m in msg:
    if (("a" <= m <= "z") or ("A" <= m <= "Z")):  # 알파벳 문자 여부 조건문
        msg2 += "★"
        print("★", end = "")

    elif ('0' <= m <= '9'):                       # 숫자 문자 여부 조건문
        msg2 += "♡"
        print("♡", end = "")

    else:        
        msg2 += m                                 # 그 외 문자 처리
        print(m, end = "") 

print()
print(msg2)                      