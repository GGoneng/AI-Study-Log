"""
내장함수 print() 사용법
- print 함수의 매개 변수 알아보기
- file 매개 변수 : 데이터를 파일에 기록
"""

# 파일 읽기 & 쓰기
# - 파일 열기 open()
# - 파일 읽기 또는 쓰기
# - 파일 닫기 close()

FILENAME = "result.txt"

# 파일을 쓰기 모드(w)로 열기

f = open(FILENAME, mode = "w")

# 파일에 데이터 출력하기

print("Good Luck", file = f)
# (or) f.write("Hello")

#파일 닫기

f.close()