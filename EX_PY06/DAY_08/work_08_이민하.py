# -------------------------------------------------------
# Unit 24
# -------------------------------------------------------

# 연습문제: 파일 경로에서 파일명만 가져오기
# 다음 소스 코드를 완성하여 파일 경로에서 파일명만 출력되게 만드세요. 
# 단, 경로에서 폴더의 깊이가 달라지더라도 파일명만 출력할 수 있어야 합니다.

path = 'C:\\Users\\dojang\\AppData\\Local\\Programs\\Python\\Python36-32\\python.exe'
path = path.split("\\")
filename = path[-1]

print(filename)

# 심사문제
# 표준 입력으로 문자열이 입력됩니다. 입력된 문자열에서 'the'의 개수를 출력하는 프로그램을 만드세요(input에서 안내 문자열은 출력하지 않아야 합니다). 
# 단, 모든 문자가 소문자인 'the'만 찾으면 되며 'them', 'there', 'their' 등은 포함하지 않아야 합니다.

import string

L = []

data = input().split()
for word in data:
    L.append(word.strip(string.punctuation))
print(L.count("the"))

# -------------------------------------------------------
# Unit 29
# -------------------------------------------------------

# 연습문제: 몫과 나머지를 구하는 함수 만들기
# 다음 소스 코드를 완성하여 x를 y로 나누었을 때의 몫과 나머지가 출력되게 만드세요.

x = 10
y = 3

def get_quotient_remainder(a, b):
    return a // b, a % b

quotient, remainder = get_quotient_remainder(x, y)
print(F"몫 : {quotient}, 나머지 : {remainder}")

# 심사문제
# 표준 입력으로 숫자 두 개가 입력됩니다. 다음 소스 코드를 완성하여 두 숫자의 덧셈, 뺄셈, 곱셈, 나눗셈의 결과가 출력되게 만드세요. 
# 이때 나눗셈의 결과는 실수라야 합니다.

x, y = map(int, input().split())

def calc(x, y):
    return x + y, x - y, x * y, x / y

a, s, m, d = calc(x, y)
print('덧셈: {0}, 뺄셈: {1}, 곱셈: {2}, 나눗셈: {3}'.format(a, s, m, d))

# -------------------------------------------------------
# Unit 30
# -------------------------------------------------------

# 연습문제: 가장 높은 점수를 구하는 함수 만들기
# 다음 소스 코드를 완성하여 가장 높은 점수가 출력되게 만드세요.

korean, english, mathematics, science = 100, 86, 81, 91
 
def get_max_score(*args):
    return max(args)
 
max_score = get_max_score(korean, english, mathematics, science)
print('높은 점수:', max_score)
 
max_score = get_max_score(english, science)
print('높은 점수:', max_score)

# 심사문제
# 표준 입력으로 국어, 영어, 수학, 과학 점수가 입력됩니다. 다음 소스 코드를 완성하여 가장 높은 점수, 가장 낮은 점수, 평균 점수가 출력되게 만드세요. 
# 평균 점수는 실수로 출력되어야 합니다.


korean, english, mathematics, science = map(int, input().split())

def get_min_max_score(*args):
    return min(args), max(args)

def get_average(**kwargs):
    sum = 0
    for arg in kwargs.values():
        sum += arg
    return sum / len(kwargs)        

min_score, max_score = get_min_max_score(korean, english, mathematics, science)
average_score = get_average(korean=korean, english=english,
                            mathematics=mathematics, science=science)
print('낮은 점수: {0:.2f}, 높은 점수: {1:.2f}, 평균 점수: {2:.2f}'
      .format(min_score, max_score, average_score))
 
min_score, max_score = get_min_max_score(english, science)
average_score = get_average(english=english, science=science)
print('낮은 점수: {0:.2f}, 높은 점수: {1:.2f}, 평균 점수: {2:.2f}'
      .format(min_score, max_score, average_score))