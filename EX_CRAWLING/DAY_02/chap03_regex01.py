import re

# 객체 생성 X
# match는 문자열의 처음부터 비교 하므로 결과값이 None

m = re.match('[a-z]+', 'Python')
print(m)
print(re.search('apple', 'I like apple!'))

# 정규식 객체 생성
p = re.compile('[a-z]+')
m = p.match('python')
print(m)
print(p.search('I like apple 123'))

m = re.match('[a-z]+', 'pythoN ')
print(m)

m = re.match('[a-z]+', 'PYthon')
print(m)

print(re.match('[a-z]+', 'regex python'))
print(re.match('[a-z]+', ' regexpython'))

# +$ 문자열의 마지막에 소문자 1회 이상 검사
print(re.match('[a-z]+', 'regexpythoN'))
print(re.match('[a-z]+$', 'regexpythoN'))

print(re.match('[a-z]+', 'regexPython'))
print(re.match('[a-z]+$', 'regexpython'))

print(re.match('[a-z]+$', 'Regex python'))


p = re.compile('[a-z]+')

print(p.findall('life is too short! Regular expression test'))


result = p.search('I like apple 123')
print(result)

result = p.findall('I like apple 123')
print(result)

