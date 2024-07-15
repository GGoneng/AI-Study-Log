"""
사용자 정의 함수
"""

# - 디폴트 매개변수 함수
# - 함수 호출 시 데이터가 전달되지 않는 경우 미리 지정된 값으로 처리
# - 형식 def 함수명(매개변수1, 매개변수2, ..., 매개변수 = 0)

def add(num1 = 0, num2 = 0):
    return num1 + num2

print(add())
print(add(5))
print(add(4, 5))


# 함수 기능 : 회원가입 기능 함수
# 함수 이름 : register
# 매개 변수 : id, pw, gender
#            성별은 기본값 "남" 지정
# 함수 결과 : "OOO님 가입을 환영합니다.", str

def register(id, pw, gender = "남"):
    return F"{id}-{gender}님 가입을 환영합니다."

print(register("kk", "k123"))
print(register("kk", "k123", "여"))

# sorted([11, 22], reverse = True)

def test(n1, n2, *nums):
    print(n1, n2, nums)

test(1, 2, 3, 4)