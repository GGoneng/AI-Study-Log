"""
==> 1줄로 조건식을 축약 : 조건부 표현식
"""

# [실습] 문자 1개 코드값을 저장하는 조건식을 작성
# - 알파벳 (a ~ z, A ~ Z) 코드값으로 변환
# - 그 외는 None으로 코드값으로 전달

data = "22"
if ("a" <= data <= "z") or ("A" <= data <= "Z"):
    print(ord(data))
else:
    print(None)

# 조건부 표현식
print(ord(data)) if ("a" <= data <= "z" or "A" <= data <= "Z") else print(None)

result = ord(data) if ("a" <= data <= "Z" or "A" <= data <= "Z") else None
print(f"{data}의 코드값 : {result}")