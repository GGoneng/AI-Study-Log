"""
List/Set/Dict 자료형과 반복문, 조건부 표현식 결합
- 메모리 사용량 감소 & 속도 빠름
"""

# [실습] A 리스트의 데이터를 B 리스트에 담기
#       단, A 리스트에서 짝수 값은 3을 곱하고, 홀수 값은 그대로
#       해서 B 리스트에 담기

a = [1, 2, 3, 4, 5, 6]
b = []
for num in a:
    if num % 2 == 0:
        b.append(num * 3)
    else:
        b.append(num)
# [1] 모든 원소를 새로운 리스트에 담기
c = [num for num in a ]
print(F"a => {a}\n b => {b}\nc => {c}")

# [2] 짝수 데이터만 새로운 리스트 C에 담기
c = [3 * num for num in a if not num % 2]
print(F"a => {a}\n b => {b}\nc => {c}")

# [3] 짝수 데이터는 3을 곱하고 홀수 데이터는 그대로 새로운 리스트 c에 담기
c = [3 * num if not num % 2 else num for num in a]
