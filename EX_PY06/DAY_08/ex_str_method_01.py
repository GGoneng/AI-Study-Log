"""
str 데이터 타입 전용 함수 즉, 메서드 살펴보기
"""

msg = "Hello 0705"
#      0123456789

# [원소 / 요소 인덱스 찾기 메서드 - find(문자 1개 또는 문자열)]
# - "H"의 인덱스
idx = msg.find("H")
print(F"H의 인덱스 : {idx}")

# - "7"의 인덱스
idx = msg.find("7")
print(F"7의 인덱스 : {idx}")

# - "llo"의 인덱스
idx = msg.find("llo")
print(F"llo의 인덱스 : {idx}")

# - "llO"의 인덱스 => 대소문자 일치, 존재하지 않으면 -1 결과로 줌
idx = msg.find("llO")
print(F"llO의 인덱스 : {idx}")

# [원소 / 요소 인덱스 찾기 메서드 - index(문자 1개 또는 문자열)]
# "H"의 인덱스
idx = msg.index("H")
print(F"H의 인덱스 : {idx}")

# "h"의 인덱스 : 존재하지 않으면 Error 발생
if "h" in msg:
    idx = msg.index("h")
    print(F"h의 인덱스 : {idx}")
else:
    print("h는 존재하지 않습니다.")

# 문자열에 동일한 문자가 여러 개 존재하는 경우
msg = "Good Luck Good"
#      01234567890123

# # - "o"의 인덱스 찾기 => 첫번째 "o" 인덱스
# idx = msg.find("o", 0)
# print(F"o의 인덱스 : {idx}")

# # - "o"의 인덱스 찾기 => 두번째 "o" 인덱스
# idx = msg.find("o", idx + 1)
# print(F"두번째 o의 인덱스 : {idx}")

# # - "o"의 인덱스 찾기 => 세번째 "o" 인덱스
# idx = msg.find("o", idx + 1)
# print(F"세번째 o의 인덱스 : {idx}")


# # - "o"의 인덱스 찾기 => 네번째 "o" 인덱스
# idx = msg.find("o", idx + 1)
# print(F"네번째 o의 인덱스 : {idx}")

idx = -1

for i in range(msg.count("o")):
    idx = msg.find("o", idx + 1)
    print(F"{i + 1}번째 o의 인덱스 : {idx}")


# 문자열의 뒷부분부터 찾기하는 메서드 ==> rfind(), rindex()
# rfind(문자, 시작인덱스, 끝인덱스 + 1) / rindex(문자, 시작인덱스, 끝인덱스 + 1)

msg = "Happy"
#      01234

# - 첫번째 "p" 인덱스 찾기
# "Happy"
#  01234
idx = msg.rfind("p")
print(F"p의 인덱스 : {idx}")

# - 두번째 "p" 인덱스 찾기
# "Happy"
#  012
idx = msg.rfind("p", 0, idx)
print(F"p의 인덱스 : {idx}")


# - 파일 명에서 확장자 txt, jpeg, xlsx, zip 찾기
# - hello.txt, 2024년상반기경제분석.doc

files = ["hello.txt", "2024년상반기경제분석.doc", "kakao_1234567898.jpg"]
for name in files:
    idx = name.find(".")
    print(name[idx + 1:])