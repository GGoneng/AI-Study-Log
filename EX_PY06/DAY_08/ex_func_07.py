"""
사용자 정의 함수
"""

# 덧셈, 뺄셈, 곱셈, 나눗셈 함수를 각각 만들기
# - 매개변수 : 정수 2개, num1, num2
# - 함수결과 : 연산 결과 반환

def add(num1, num2):
    print(num1 + num2)

def sub(num1, num2):
    print(num1 - num2)

def mul(num1, num2):
    print(num1 * num2)

def div(num1, num2):
    if num2 == 0:
        print("0으로 나눌 수 없음")
    else:
        print(num1 / num2)

# 함수 사용하기 
add(1, 4)
sub(7, 3)
mul(3, 2)
div(6, 2)

# 함수 기능 : 입력 데이터가 유효한 데이터인지 검사해주는 기능
# 함수 이름 : check_data
# 매개 변수 : 문자열 데이터, 데이터 갯수 data, count, sep = " "
# 함수 결과 : 유효 여부 boolean
def check_data(data, count, sep = " "):
    # 데이터 여부
    if len(data):
        data2 = data.split(sep)
        return True if count == len(data2) else False
    # 데이터 분리 후 갯수 체크
    else:
        return False

print(check_data("+ 10 3", 3))
print(check_data("+ 10", 3))
print(check_data("+ 10 3 5", 3))


# [실습] 사용자로부터 연산자, 숫자1, 숫자2를 입력 받아서
# 연산 결과를 출력해주세요.
# - input("연산자, 숫자1, 숫자2 : ").split()

# op, num1, num2 = input("연산자, 숫자1, 숫자2 : ").split(" ")

# num1 = int(num1)
# num2 = int(num2)

# if op == "+":
#     add(num1, num2)

# elif op == "-":
#     sub(num1, num2)

# elif op == "*":
#     mul(num1, num2)

# elif op == "/":
#     div(num1, num2)

# else:
#     print("잘못된 연산자 입니다.")