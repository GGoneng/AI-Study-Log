"""
사용자 정의 함수
"""

# 목적 : 매개변수의 개수를 유동적으로
#        0개 ~ N개 까지 가능하도록
# 형태 : def 함수명(*변수명) <= 0개 ~ N개 데이터

# 함수 기능 : 정수를 덧셈 한 후 결과를 출력해주는 함수
# 함수 이름 : add
# 매개 변수 : 0개 ~ N개
# 함수 결과 : 덧셈 계산 값 result

def add(*nums):
    total = 0
    for n in nums:
        total += n
    return total

# 함수 호출
print(add())
print(add(1, 1, 1))
print(add(5, 6))
print(add(8, 9, 11, 22, 55, 11, 6, 7))
