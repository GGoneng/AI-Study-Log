"""
람다 표현식 또는 람다 함수
- 1줄 함수, 익명 함수
- 형식 : lambda 매개변수 : 실행코드
"""

names = {1 : "Kim", 2 : "Adam", 3 : "Zoo"}

# 정렬하기 => 내장함수 sorted() --> list 반환
# key로 정렬
result = sorted(names)
print("오름차순 정렬 [Key]", result)

# value로 정렬 => names.items() --> (1, "Kim"), (2, "Adam"), (3, "Zoo")
result = sorted(names.items(), key = lambda items : items[1])
print("오름차순 정렬 [Value]", result)

result = sorted("This is a test string from Andrew".split())
print(result)

result = sorted("This is a test string from Andrew".split(), key = str.lower)
print(result)


# map()와 lambda
data = [11, 22, 33, 44]

# - 각 원소의 값에 곱하기 2를 해서 다시 리스트로 저장
def multi2(value):
    return value * 2

data2 = list(map(lambda a : a * 2, data))
print(data2)
