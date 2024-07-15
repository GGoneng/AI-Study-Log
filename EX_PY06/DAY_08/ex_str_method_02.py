"""
str 데이터 타입 전용 함수 즉, 메서드 살펴보기
"""

# [문자열에서 좌우 여백 제거 메서드 -> strip(), lstrip(), rstrip()]
# - 주의 : 문자열 내부의 공백은 제거 X

msg = "Good Luck"
data = " Happy New Year 2025!  "

# 좌우 모든 공백 제거
m1 = msg.strip()
print(F"원본 msg : {len(msg)}개 --- 제거 m1 : {len(m1)}개")

m2 = data.strip()
print(F"원본 msg : {len(data)}개 --- 제거 m2 : {len(m2)}개")


# 왼쪽 즉, 문자열 시작 부분의 공백 제거
m2 = data.lstrip()
print(F"원본 msg : {len(data)}개 --- 제거 m2 : {len(m2)}개")

m2 = data.rstrip()
print(F"원본 msg : {len(data)}개 --- 제거 m2 : {len(m2)}개")


# [실습] 이름을 입력 받아서 저장하세요.
# - input()함수 사용

name = input("이름 : ").strip()

if len(name) > 0 :
    print(F"name : {name}")
else:
    print("입력하지 않았습니다.") 

# [실습] 입력 받은 데이터에 따라 출력을 다르게 합니다
# - input()함수 사용
# - [조건] 알파벳이면 ★, 숫자면 ♥, 나머지는 무시 <== if문 사용

data = input("알파벳, 숫자 또는 문자 1개 입력 : ")

if "a" <= data <= "z" or "A" <= data <= "Z":
    print("★")
elif "0" <= data <= "9":
    print("♥")

