"""
제어문 - 반복문
"""

# [실습] 문자열을 기계어 즉, 2진수로 변환해서 저장하기
# - [입력] Hello
# - [출력] 101111010110001

data = "Hello"
result = ""
for char in data:
    result += bin(ord(char))[2:]
    print(result)

# [실습] 원소 / 요소의 인덱스와 값을 함께 가져오기
# enumerate() 내장 함수
# - 전달된 반복 가능한 객체에서 원소당 번호를 부여해서 튜플로 묶어줌
# - 원소의 인덱스 정보가 필요한 경우 사용

nums = [1, 3, 5]

# 원소 데이터만 가져오기
for n in nums: print(n)

# enumerate() : 원소에 인덱싱 부여한 객체 변환
print("enumerate() 변환 : ", list(enumerate(nums)))

# 인덱스와 원소 데이터 가져오기
for idx, data in enumerate(nums):
    print(idx, data)
    nums[idx] = int(data)

# e = (0, 1)
for e in enumerate(nums):
    print(e[0], e[1])
    nums[e[0]] = int(e[1])