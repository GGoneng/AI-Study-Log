"""
사용자 정의 함수 - 실습
"""

# 함수 기능 : 원하는 단의 구구단을 출력해주는 기능 함수
# 함수 이름 : gugudan
# 매개 변수 : dan
# 함수 결과 : None

def gugudan(dan):
    for i in range(1, 10):
        print(F"{dan} * {i} = {dan * i}")

# 함수 기능 : 파일의 확장자를 반환해주는 기능 함수
# 함수 이름 : extract
# 매개 변수 : file
# 함수 결과 : None

def extract(file):
    print(file[file.rfind(".") + 1:])

# 함수 사용
gugudan(3)

extract("abc.txt")
extract("file.xml")