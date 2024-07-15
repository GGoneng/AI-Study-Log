"""
연산자 - 객체 비교 연산자
** 객체
    힙 영역에 존재하는 데이터 즉, 저장된 데이터
    클래스를 기반으로 저장됨
"""
num1 = "Hello"
num2 = num1

# 2개의 변수가 동일한 객체를 저장하고 있는지 확인
# 연산자 => 객체 비교 연산자

print(f"num1 is num2 => {num1 is num2}")
print(f"num1 id : {id(num1)}")
print(f"num2 id : {id(num2)}")

num2 = "hello"

print(f"num1 is num2 => {num1 is num2}")
print(f"num1 id : {id(num1)}")
print(f"num2 id : {id(num2)}")

# 비교 연산자 : 크기 비교
print(f"{num1} == {num2} : {num1 == num2}")
