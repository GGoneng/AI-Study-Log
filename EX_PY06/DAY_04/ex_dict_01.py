# 강아지에 대한 정보 : 품종, 

# [Dict 원소 / 요소 읽기]
# - 키를 가지고 값 / 데이터 읽기

data = {"age" : 5, "kind" : "허스키", "weight" : "3kg", "color" : "검정", "gender" : "남"}

# 색상 출력
print(f"색상 : {data['color']}")

# 성별, 품종 출력
print(f"강아지 성별 : {data['gender']},  품종 : {data['kind']}")

# [Dict 원소 / 요소 변경]
# - 변수명[key] = 새로운 값
# 나이 5살 ==> 6살

data["age"] = "6살"
print(f"강아지 나이 : {data['age']}")

# 몸무게 3kg ==> 8kg

data["weight"] = "8kg"
print(f"강아지 무게 : {data['weight']}")

# - del 변수명[key] 또는 del(변수명[key])
# 성별 데이터 삭제

del data["gender"]
print(data)

# 추가 : 변수명[새로운 키 ] = 값
# 이름 추가

data["name"] = "뽀삐"  
print(data)

data["name"] = "허숙희"
print(data)