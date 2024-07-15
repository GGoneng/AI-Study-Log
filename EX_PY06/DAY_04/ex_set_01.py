"""
Set 자료형 살펴보기
- 여러 가지 종류의 여러 개 데이터를 저장
- 단! 중복 안됨!!!
- 컬렉션 타입의 데이터 저장 시 Tuple 가능
- 형태 : {데이터1, 데이터2, ..., 데이터n}
"""

# [Set 생성]
data = set()
print(F"data의 타입 : {type(data)}, 원소 / 요소 개수 : {len(data)}개, 데이터 : {data}")

# 여러 개 데이터 저장한 set
data = {10, 30, 20, -9, 10, 30, 10, 30, 10, 10}
print(F"data의 타입 : {type(data)}, 원소 / 요소 개수 : {len(data)}개, 데이터 : {data}")

data = {9.34, "Apple", 10, True, "10"}
print(F"data의 타입 : {type(data)}, 원소 / 요소 개수 : {len(data)}개, 데이터 : {data}")

# data = {1, 2, 3, [1, 2, 3]}
# data  = {1, 2, 3, (1, 2, 3)}
# data  = {1, 2, 3, (1)}
data  = {1, 2, 3, (1,)}
# data2 = {1, 2, 3, data} - set은 변경이 가능한 타입이라서 ERROR
print(F"data의 타입 : {type(data)}, 원소 / 요소 개수 : {len(data)}개, 데이터 : {data}")

# set() 내장 함수
data = {1, 2, 3} # ====> set([1, 2, 3])
data = set()     # Empty Set
data = set({1, 2, 3})

# 다양한 타입 ==> set 변환
data = set([1, 2, 1, 2, 3])
data = set("Good")
data = set({"name" : "홍길동", "age" : 12, "name" : "배트맨"})
data = set((1, 2, 1, 2, 1))
print({"name" : "홍길동", "age" : 12, "name" : "배트맨"})
print(data)

