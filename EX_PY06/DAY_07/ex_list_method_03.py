"""
리스트 전용의 함수 즉, 메서드(Method)
- 리스트의 원소 / 요소를 제어하기 위한 함수들
"""

import copy

datas = [11, 22, 33]
nums = datas
print(F"datas => {datas}\nnums => {nums}")

nums[0] = "백"
print(F"datas => {datas}\nnums => {nums}")

# 메서드 - 리스트 복사해주는 메서드 copy()
# 얕은 복사 ---> 깊은 복사는 모듈 추가
nums2 = datas.copy()
nums3 = copy.deepcopy(datas)
datas[0] = "A"

print(F"datas => {datas}\nnums => {nums}\nnums2 => {nums2}\n nums3 => {nums3}")