"""
제어문 - while 반복문
"""

num = 10
while num > 0:
    num = num - 1
    print(num)
# [실습] 리스트의 원소 읽기
# - while 반복문 : 개수

nums = [11, 22, 33]

count = 0
while count < len(nums):
    print(nums[count])
    count += 1

# [실습] "Hello" 문자열의 원소를 하나씩 출력하기
msg = "Hello"
#      01234

idx = 0

while idx < len(msg):
    print(msg[idx])
    idx += 1
