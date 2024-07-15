"""
str 데이터 타입 전용 함수 즉, 메서드 살펴보기
"""

# [문자열을 구성하는 문자를 검사해주는 메서드]
# - isXXXX() ---> 결과 논리형 True / False
# [1] 알파벳으로 구성된 문자열인지 검사 isalpha()

data = "good"
print(F"{data} => {data.isalpha()}")


# [2] 알파벳으로 구성도니 문자열인지 대문자인지 검사 : isupper()
data = "good"
print(F"{data} => {data.isupper()}")
print(F"GOOD => {'GOOD'.isupper()}")
print(F"Good => {'Good'.isupper()}")

# [3] 알파벳으로 구성된 문자열인지 소문자인지 검사 : islower()
print(F"GOOD => {'GOOD'.isupper()}")
print(F"Good => {'Good'.isupper()}")
print(F"good => {'good'.isupper()}")

# [4] 숫자로 구성된 문자열인지 검사 : isdecimal()
print(F"1234 => {'1234'.isdecimal()}")
print(F"Happy1234 => {'Happy1234'.isdecimal()}")


# [5] 숫자와 문자가 혼합된 문자열인지 검사 : isalnum()
print(F"1234 => {'1234'.isalnum()}")
print(F"Happy1234 => {'Happy1234'.isalnum()}")
print(F"Happy => {'Happy'.isalnum()}")


# [6] 공백 문자 여부 검사 : isspace()
print(F"1234    = > {'1234     '.isspace()}")
print(F"         => {'   '.isspace()}")

# -----------------------------------------------------------------------------
# 문자열 구성하는 문자 검사 메서드 => 변수명.isOOO()
# -----------------------------------------------------------------------------
# 문자열 내에 숫자 존재여부 체크 메서드들 3종류
# - 변수명.isnumeric()  : 0~9까지의 숫자, 5¹, 5₁, ①, ➊, ⅒, Ⅳ, ⅳ, 百
# - 변수명.isdigit()    : 0~9까지의 숫자, 5¹, 5₁, ①, ➊ 
# - 변수명.isdecimal()  : 0~9까지의 숫자
#    ==> 실수, 음수, 나머지 : False
# - isdecimal() < isdigit() < isnumeric()
# -----------------------------------------------------------------------------