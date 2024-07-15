"""
Tuple 데이터 자료형 살펴보기
- 내장 함수 : len(), max(), min(), sum()
- 연산자 : 덧셈, 곱셈, 멤버 연산자
"""

nums = 11, 22, 33, 44, 55

# 내장 함수
print(f"nums 개수 : {len(nums)}개")
print(f"최대값 : {max(nums)} 최소값 : {min(nums)}")
print(f"합계 : {sum(nums)}")
print(f"정렬 : {sorted(nums)}, {sorted(nums, reverse = True)}")

print(max("abc", "abC"))
print(sorted(["abc", "Zoo"]))
print(sum([11, 22]))


# 연산자
# 덧셈
data1 = 11, 22
data2 = "A", "B", "C"
data3 = [1, 2]

print(data1 + data2) # tuple + tuple
print(data1 + tuple(data3)) # tuple + list

# 곱셈 : tuple * int
print(data1 * 3)

# 멤버 연산자 => in, not in
print(11 in data1) 
print("A" in data1)
