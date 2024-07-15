"""
==> 조건부 표현식 : 조건이 2개 이상인 경우
"""

# [실습] 숫자가 양수, 영 음수 인지 판별
num = int(input())

print("양수") if num > 0 else print("영") if num == 0 else print("음수")