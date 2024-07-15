"""
사용자 정의 함수
"""

# - 매개변수의 전달되는 데이터가 지정되지 않는 경우
# - 데이터 종류 = 데이터 ==> 키워드 파라미터 / 키워드 매개변수
# - 형식 def 함수명 (**params) => 키 = 값

# 함수 기능 : 회원가입 기능 함수
# 함수 이름 : register
# 매개 변수 : 가입하는 사람마다 입력하는 정보가 모두 다름 **params
# 함수 결과 : 가입 메시지 str

def register(**params):
    print(type(params))

register(name = "홍길동", job = "의적")
register(id = "master", age = 10, gender = "F")
register()


# 함수 기능 : 회원가입 기능 함수
# 함수 이름 : register2
# 매개 변수 : 필수 입력 사항 id, pw, email
#            선택 입력 사항 **params
# 함수 결과 : 가입 메시지 str

def register2(id, pw, email, **params):
    print(type(params))

register2("Hong", "H12345", "h@naver.com", gender = "F")
register2("Hong", "H12345", "h@naver.com")
# register2("Hong", "H12345") # ERROR
