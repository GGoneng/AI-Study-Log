"""
함수(Function) 이해 및 활용
"""

# 함수 기능 : 3개의 정수를 덧셈한 후 결과를 반환하는 함수
# 함수 이름 : add3
# 매개 변수 : num1, num2, num3
# 함수 결과 : 정수 result

def add3(num1, num2, num3):
    result = num1 + num2 + num3
    return result


# 함수 기능 : 3개의 정수를 곱셈한 후 결과를 반환하는 함수
# 함수 이름 : multi3
# 매개 변수 : num1, num2, num3
# 함수 결과 : 정수 result

def multi3(num1, num2, num3):
    result = num1 * num2 * num3
    return result


# 함수 기능 : 2개의 정수를 나눗셈한 후 결과를 출력하는 함수
# 함수 이름 : div
# 매개 변수 : num1, num2
# 함수 결과 : None

def div(num1, num2):
    if num2 == 0:
        result = "0으로 나눌 수 없음"
    else:
        result = num1 / num2
    print(result)

# 함수 사용하기 즉, 호출
# 덧셈하기
value = add3(1, 2, 3)

# 나눗셈하기
value1 = div(3, 4)

print(value1)
