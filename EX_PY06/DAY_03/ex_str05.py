"""
문자열 str 데이터 다루기
- 이스케이프 문자 : 특수한 의미를 가지는 문자
    * 형식 : \문자 1개
    * '\n' - 줄바꿈 문자
    * '\t' - 탭 간격 문자
    * '\'' - 홑따옴표 문자
    * '\"' - 쌍따옴표 문자
    * '\\' - \ 백슬러시 문자, 경로(path), URL 관련

    * '\a' - 알람소리 문자
"""

msg = "오늘은 좋은 날\n내일은 주말이라 행복해"
print(f"msg 줄바꿈 : {msg}")

msg = '오늘은 나의 "생일"이야'
print(msg)

#  r' ' 또는 R'  ' : 문자열 내 이스케이프 문자는 무시됨
file = r'C:\\Users\\KDP-2\\Python\\test.txt'
print(file)

msg = "Happy\tNew\tyear"
msg2 = R"Happy\tNew\tyear"
print(msg, msg2)