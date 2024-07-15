"""
조건부 표현식
- 조건문을 1줄로 축약해주는 문법
- 다중 조건문을 축약할 때 사용
- 다른 프로그래밍 언어에서 삼항연산자와 유사
- 형식 : 참 일때, 실행 코드 if 조건식 else 거짓실행 코드
"""

# [실습] 임의의 숫자 데이터를 정하기
#        해당 숫자 데이터가 짝수 인지 홀수 인지 판별 하는 코드

num = int(input())

print(f"{num} is even") if num % 2 == 0 else print(F"{num} is odd")
print("홀수") if num % 2 else print("짝수")
print("짝수") if not num % 2 else print("홀수")
