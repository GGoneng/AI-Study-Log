"""
사용자 정의 함수
"""
# 함수 기능 : 2개 정수를 덧셈 한 후 결과를 출력해주는 함수
# 함수 이름 : add
# 매개 변수 : 2개, num1, num2
# 함수 결과 : 없음

def add(num1, num2):
    result = num1 + num2
    print(F"{num1} + {num2} = {result}")

add(5, 8)

# 함수 기능 : 인사 메시지를 출력하는 함수
# 함수 이름 : hello
# 매개 변수 : 없음
# 함수 결과 : 없음

def hello():
    print("hello")

hello()