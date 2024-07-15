"""
내장함수 print() 사용법
- 모니터, 콘솔 / 터미널에 출력하는 함수
- 문법 : print(argument1, argument2, ...)
         print()
"""

# 나이, 이름, 성별을 저장하기

age = 100
name = "마징가"
gender = "남자"

# 모니터에 출력하기

print(age)
print(name)
print(gender)

# 한 줄에 3개 모두 출력하기

print(age, name, gender)
print(99, "홍길동", "여자")

# 2개의 정수 덧셈 결과 출력하기

num1 = 2
num2 = 9
print(num1 + num2)

# 출력 결과 => 2 + 9 = 11

print(num1, "+", num2, "=", num1 + num2)

# 서식 지정자(Format String) 방식
# ==> 화면 출력 글자를 만들고 그 글자 안에 특정 결과를 출력하는 형식
# ==> 글자 내부에 정수 결과 넣기 : ' %d ' %변수명 또는 %수식 
# ==> 글자 내부에 실수 결과 넣기 : ' %f ' %변수명 또는 %수식 
# ==> 글자 내부에 글자 결과 넣기 : ' %s ' %변수명 또는 %수식 
# 2 + 9 = 11를 서식 지정자를 활용하여 화면에 출력

print("%d + %d = %d" %(num1, num2, (num1 + num2)))

# 9 / 2 = 4.5 화면에 출력
print("%d / %d = %f" %(num2, num1, (num2 / num1)))
print("%s / %s = %s" %(num2, num1, (num2 / num1)))

# ==> F-String 방식
# ==> 형식 : f' {변수명 또는 수식, 또는 데이터} '
# ==> 형식 : F' {변수명 또는 수식, 또는 데이터} '
# 2 + 9 = 11를 F-String을 활용하여 화면에 출력

print(f'{num1} + {num2} = {num1 + num2}')

# 9 / 2 = 4.5 화면에 출력

print(f"{num2} / {num1} = {num2 / num1}")