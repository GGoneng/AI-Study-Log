"""
==> 1줄로 조건식을 축약 : 조건부표현식
"""
# [실습] 임의의 숫자가 5의 배수인지 아닌지 결과를 출력 하세요.
#        단, 5를 제외한 나머지는 고려하지 X

# num = int(input())
# print("5의 배수 O") if num % 5 == 0 else print("2의 배수 O") if num % 2 == 0 else print("아무것도 아님")

# num = int(input())
# print("5의 배수 O") if num % 5 == 0 else print("5의 배수 X")

# [실습] 문자열을 입력 받아서 문자열의 원소 개수를 저장
# - 단, 원소 개수가 0이면 None 저장

# data = input()
# # result = len(data)
# if len(data):
#     result = len(data)
# else:
#     result = None

# result = len(data) if len(data) else None

# print(F"{data}의 원소 / 요소 개수 : {result}개")

# [실습] 연산자(4칙 연산자 : +, -, *, /)와 숫자 2개 입력 받기
# - 입력된 연산자에 따라 계산 결과 저장
# - 예) + 10 3    출력 : 13

option, num1, num2 = input().split()
num1 = int(num1); num2 = int(num2)
if option == "+":
    result = num1 + num2

elif option == "-":
    result = num1 - num2

elif option == "*":
    result = num1 * num2

elif option == "/":
    result = num1 / num2

print(result)

result = num1 + num2 if option == "+" else num1 - num2 if option == '-' else num1 * num2 if option == "*" else num1 / num2 if option == "/" else None
print(result)