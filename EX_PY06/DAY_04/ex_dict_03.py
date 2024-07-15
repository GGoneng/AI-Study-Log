"""
Dict 자료형 살펴보기
- Dict 자료형 전용의 함수 즉, 메서드(Method) 사용
- 사용법 : 변수명.메서드명()
"""

# [Dict에서 키만 추출하는 메서드 keys()]
p1 = {"name" : "홍길동", "age" : 20, "job" : "학생"}

result = p1.keys()
print(f"키 추출 : {result}, {type(result)}")
# ERROR : print(result[0])

# list 형변환 => list(dict_keys타입)
result = list(result)
print(f"키 추출 : {result}, {type(result)}")

# [Dict에서 값 / 데이터만 추출하는 메서드 values()]
result = p1.values()
print(f"값 추출 : {result}, {type(result)}")

# [Dict에서 키와 값 데이터를 추출하는 메서드 items()]
result = p1.items()
print(F"키와 값 묶음 추출 : {result}, {type(result)}")

result = list(result)
print(F"키와 값 묶음 추출 : {result[0]}, {type(result[0])}")
