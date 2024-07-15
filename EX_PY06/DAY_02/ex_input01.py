"""
내장함수 input() 사용법
- 키보드로부터 입력한 데이터 받아오는 내장 함수
- 문법 : input("요청 문자열")
- 특징 : 입력 후 Enter키 입력이 되어야지만 데이터 전달 됨
         즉, 입력이 완료될 때까지 멈춤
"""

# 이름 입력 받기
name = input("이름? ")

# OOO님 맛점!
print(f"{name}님 맛점!")
print("%s님 맛점!" %name)
print(name, "님 맛점!")
print(name, end = "")
print("님 맛점!")
