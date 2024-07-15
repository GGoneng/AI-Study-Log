# [실습] 10번 숫자 데이터를 입력을 받습니다.
#        - 숫자 데이터를 모두 더해서 합계가 30 이상이 되면
#          10번 입력 안 받았더라도 종료해주세요.

data = 0

for i in range(10):
    data += int(input("숫자 데이터를 입력하세요 : "))
    if data >= 30:
        break

print(data)