"""
리스트 전용의 함수 즉, 메서드(Method)
- 리스트의 원소 / 요소를 제어하기 위한 함수들
"""
# [메서드 - 요소 추가 메서드 append(데이터)]
datas = [1, 3, 5]

# 새로운 데이터 100 추가 : 제일 마지막 원소 추가
datas.append(100)
print(F"datas 개수 : {len(datas)}, {datas}")

datas.append(100)
print(F"datas 개수 : {len(datas)}, {datas}")

# [메서드 - 요소 추가 메서드 insert(인덱스, 데이터)]
datas.insert(0, 300)
print(F"datas 개수 : {len(datas)}, {datas}")

datas.insert(-1, 300)
print(F"datas 개수 : {len(datas)}, {datas}")

# [실습 : 임의의 정수 숫자 10개 저장하는 리스트 생성]

import random

L = []

for i in range(10):
    L.append(int(random.random() * 10))
print(L)

# [메서드 - 요소 삭제 메서드 remove(데이터)]
# datas 개수 : 7, [300, 1, 3, 5, 100, 300, 100]
# - 존재하지 않는 데이터 삭제 시 ERROR 발생함!

for cnt in range(datas.count(300)):
    datas.remove(300)
    print(F"datas 개수 : {len(datas)}, {datas}")

# [메서드 - 요소 순서 제어 메서드 reverse()]

import random

random.seed(10) # 동일한 랜덤 숫자 추출을 위한 기준점
datas = []
for _ in range(10):
    datas.append(random.randint(1, 30))

print(f"{len(datas)}개, {datas}")

# 0번 => -1번으로, -1 => 0번으로 위치 변경
datas.reverse()
print(F"{len(datas)}개, {datas}")

# [메서드 - 요소 크기를 비교해서 정렬해주는 메서드 sort()]
# - 기본 정렬 : 오름차순 즉, 작은 데이터부터 큰 데이터 순서로

datas.sort()
print(F"{len(datas)}개, {datas}")

# - 내림차순 즉, 큰 데이터부터 작은 데이터 순서로
datas.sort(reverse = True)
print(F"{len(datas)}개, {datas}")

# [메서드 - 리스트에서 요소를 꺼내는 메서드 pop()]
# - 리스트에서 요소가 삭제됨
value = datas.pop() # 제일 마지막 뭔소 / 요소 꺼내기
print(F"value : {value} - {len(datas)}개, {datas}")

value = datas.pop(0) # 특정 인덱스의 원소 / 요소 꺼내기
print(F"value : {value} - {len(datas)}개, {datas}")

# [메서드 - 리스트 확장 시켜주는 메서드 extend()]
datas.extend([11, 22, 33])
print(F"{len(datas)}개, {datas}")

datas.extend((555, 777))
print(F"{len(datas)}개, {datas}")

datas.extend({555, 777, 555, 777})
print(F"{len(datas)}개, {datas}")

datas.extend({"name" : "홍길동", "age" : 12})
print(F"{len(datas)}개, {datas}")

# [메서드 - 모든 원소 삭제 메서드 clear()]
datas.clear()
print(F"{len(datas)}개, {datas}")

