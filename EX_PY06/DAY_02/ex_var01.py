"""
변수와 메모리 관계
- 파이썬에서 사용하는 변수 -> 참조형 변수
- 메모리 힙 영역에 저장된 데이터의 주소 저장
-> 주소 확인 내장 함수 : id(변수명 또는 데이터)
"""

# 나이를 저장하기
age = 27
number = 27

# 데이터가 존재하는 주소 확인
print(id(age))
print(id(27))
print(id(number))

age = 100

print(id(age))
print(id(27))
print(id(number))
print(id(100))