"""
제어문 - 반복문과 조건문 혼합
"""

# [실습]
# 메시지를 입력 받습니다.
# 알파벳 대문자인 경우 소문자로, 소문자인 경우 대문자로
# 나머지는 그대로 되도록 출력하기
# 코드값 32 차이

# 문자 ==> 코드 : ord(문자 1개)
# 코드 ==> 문자 : chr(정수 코드값)

msg = input("메시지를 남겨주세요 : ")
result = ""

for m in msg:
    # 소문자 ==> 대문자
    if ("a" <= m <= "z"):
        result += chr(ord(m) - 32)
    
    # 대문자 ==> 소문자
    elif ("A" <= m <= "Z"):
        result += chr(ord(m) + 32)
    
    else:
        result += m

print(result)