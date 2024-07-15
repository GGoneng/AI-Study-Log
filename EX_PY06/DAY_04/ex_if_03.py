"""
중첩 조건문
- 조건문에 조건문이 존재하는 제어문
- 형식
    if 조건식:
        실행코드
        if 조건식:
            실행코드
            실행코드
"""

# [실습] 숫자가 음이 아닌 정수와 음수 구분하기
#        음이 아닌 정수 중에 0과 양수 구분하기

num = int(input("숫자를 입력하시오. : "))

if (num >= 0):
    print(F"숫자 {num}은 음이 아닌 정수입니다.")
    
    if(num == 0):
        print(F"숫자 {num}은 0입니다.")
    
    else:
        print(F"숫자 {num}은 양수입니다.")

else:
    print(F"숫자 {num}은 음수 입니다.")

# 다중 조건문으로
if num > 0:
    print(f"{num}은 양수")

elif num < 0:
    print(F"{num}은 음수")

else:
    print(F"{num}은 0")


# 동네 이름 데이터에서 입력 받은 동네 이름 해당 여부
city = ["대구", "부산", "울산"]
data = "마산"

if data in city:
    print(F"{data}는 광역시입니다.")