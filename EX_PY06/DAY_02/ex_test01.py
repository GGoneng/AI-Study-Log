"""
입력 & 출력 실습

[실습1] 데이터 저장 및 변수 생성
- 생년월일
- 띠 (용, 범...)
- 혈액형
- 출력형태
  나는 0000년 00월 00일 000띠입니다.
  혈액형은 

[실습2] 입력 받은 데이터 저장 단, 파일로 저장
- 좋아하는 계절
- 좋아하는 나라
- 여행가고 싶은 나라
"""

# 실습1
birth = "20000512"
chinese_zodiac = "용"
blood = "O"

print("나는 %s년 %s월 %s일 %s띠입니다." %(birth[0:4], birth[4:6], birth[6:], chinese_zodiac))
print("혈액형은 성격 좋은 %s형입니다.\n" %(blood))

# 실습2

season = input("좋아하는 계절을 입력하시오 : ")
like_country = input("좋아하는 나라를 입력하시오 : ")
want_country = input("여행가고 싶은 나라를 입력하시오 : ")

FILENAME = "result.txt"

f = open(FILENAME, mode = "w", encoding = 'UTF-8')
# f.write("좋아하는 계절 : %s\n" %(season))
# f.write("좋아하는 나라 : %s\n" %(like_country))
# f.write("여행가고 싶은 나라 : %s\n" %(want_country))

print(f'좋아하는 계절       : {season}', file = f)
print(f'좋아하는 나라       : {like_country}', file = f)
print(f'여행가고 싶은 나라   : {want_country}', file = f, end = '')
f.close()
