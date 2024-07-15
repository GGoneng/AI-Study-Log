"""
함수(Function) 이해 및 활용
함수 기반 계산기 프로그램
- 4칙 연산 기능별 함수 생성 => 덧셈, 뺄셈, 곱셈, 나눗셈
- 2개 정수만 계산
"""

def add(num1, num2):
    return num1 + num2

def sub(num1, num2):
    return num1 - num2

def mul(num1, num2):
    return num1 * num2

def div(num1, num2):
    if num2 == 0:
        return "잘못된 값입니다."
    else:    
        return num1 / num2

# 사용자가 종료를 원할때 종료 => "x", "X" 입력 시
# - 연산방식과 숫자 데이터 입력 받기

while True:    
    data = input("기호, 숫자1, 숫자2 : ")
    
    if data == "x" or data == "X":
        print("계산기를 종료합니다")
        break
    
    op, num1, num2 = data.split()
    num1 = int(num1); num2 = int(num2)

    if op == "+":
        print(add(num1, num2))

    elif op == "-":
        print(sub(num1, num2))
    
    elif op == "*":
        print(mul(num1, num2))

    elif op == "/":
        print(div(num1, num2))
    
    else:
        print(F"{op}는 지원되지 않는 연산입니다.")