"""
반복문과 continue
- continue 구문을 만나면 구문 아래 코드 실행 X
- 반복문으로 가서 다음 요소 데이터를 가지고 진행
"""

# [실습] 1 ~ 50까지 숫자로 구성된 데이터
# 3의 배수 인 경우만 화면에 출력하세요.

data = list(range(1, 51))
for num in data:
    if num % 3:
        continue
    print(F"{num}", end = " ")