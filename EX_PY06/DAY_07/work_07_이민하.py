# -------------------------------------------------------
# Unit 22
# -------------------------------------------------------

# 연습문제: 리스트에서 특정 요소만 뽑아내기
# 다음 소스 코드를 완성하여 리스트 a에 들어있는 문자열 중에서 길이가 5인 것들만 리스트 형태로 출력되게 만드세요(리스트 표현식 사용).

a = ['alpha', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india']
b = [i for i in a if len(i) == 5]

print(b)

# 심사문제
# 표준 입력으로 정수 두 개가 입력됩니다(첫 번째 입력 값의 범위는 1~20, 두 번째 입력 값의 범위는 10~30이며 첫 번째 입력 값은 두 번째 입력 값보다 항상 작습니다). 첫 번째 정수부터 두 번째 정수까지를 지수로 하는 2의 거듭제곱 리스트를 출력하는 프로그램을 만드세요(input에서 안내 문자열은 출력하지 않아야 합니다). 단, 리스트의 두 번째 요소와 뒤에서 두 번째 요소는 삭제한 뒤 출력하세요. 
# 출력 결과는 리스트 형태라야 합니다.

start, end = map(int, input().split())

result = [2 ** i for i in range(start, end + 1)]
result.pop(1)
result.pop(-2)
print(result)

# -------------------------------------------------------
# Unit 25
# -------------------------------------------------------

# 연습문제: 평균 점수 구하기
# 다음 소스 코드를 완성하여 평균 점수가 출력되게 만드세요.

maria = {'korean': 94, 'english': 91, 'mathematics': 89, 'science': 83}
average = sum(maria.values()) / len(maria)                     
print(average)

# 심사문제
# 표준 입력으로 문자열 여러 개와 숫자 여러 개가 두 줄로 입력되고, 첫 번째 줄은 키, 두 번째 줄은 값으로 하여 딕셔너리를 생성합니다. 
# 다음 코드를 완성하여 딕셔너리에서 키가 'delta'인 키-값 쌍과 값이 30인 키-값 쌍을 삭제하도록 만드세요.

keys = input().split()
values = map(int, input().split())

x = dict(zip(keys, values))

x = {key : value for key, value in x.items() if key != "delta" and value != 30}
print(x)