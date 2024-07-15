"""
Tuple 전용 함수 즉, 메서드
- 수정 불가 즉, 추가, 삭제, 변경 X
"""

nums = 10, 20, 30

# 메서드 - 인덱스 확인 메서드 index(데이터)
idx = nums.index(20)
print(idx)

if 5 in nums:
    idx = nums.index(5)
    print(idx)

# 메서드 - 데이터 개수 메서드 count(데이터)
print(10, nums.count(10))
print(5, nums.count(5))
