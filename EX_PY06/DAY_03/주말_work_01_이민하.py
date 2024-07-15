# -------------------------------------------------------
# Print 기초
# -------------------------------------------------------

# 001.
print("Hello world")

# 002.
print("Mary's cosmetics")

# 003.
print("신씨가 소리질렀다. \"도둑이야\".")

# 004.
print("C:\Windows")

# 005.
print("안녕하세요.\n만나서\t\t반갑습니다.")
#\t : 탭 띄어쓰기, \n : 줄 바꿈

# 006.
print("오늘은", "일요일")
# 출력 결과 : 오늘은 일요일

# 007.
print("naver", "kakao", "sk", "samsung", sep = ";")

# 008.
print("naver", "kakao", "sk", "samsung", sep = "/")

# 009.
print("first", end =""); print("second")

# 010.
print(5/3)

# 011.
삼성전자 = 50000
print(삼성전자 * 10)

# 012.
시가총액 = 298000000000000
현재가 = 50,000
PER = 15.79

# 013.
s = "hello"
t = "python"

print(f"{s}! {t}")

# 014.
print(2 + 2 * 3)
# 결과 : 8

# 015.
a = "132"
print(type(a))
# 결과 : <class 'str'>

# 016.
num_str = "720"
num = int(num_str)
print(num, type(num))

# 017.
num = 100
str_num = str(num)
print(str_num, type(str_num))

# 018.
num = "15.79"
float_num = float(num)
print(float_num, type(float_num))

# 019.
year = "2020"
year = int(year)
print(year - 2, year - 1, year)

# 020.
monthly_cost = 48584
month = 36
print(f"{monthly_cost} * {month} = {monthly_cost * month}")

# 021.
letters = 'python'
print(letters[0], letters[2])

# 022.
license_plate = "24가 2210"
print(license_plate[4:])

# 023.
string = "홀짝홀짝홀짝"
print(string[::2])

# 024.
string = "PYTHON"
print(string[::-1])

# 025.
phone_number = "010-1111-2222"
a = phone_number.split("-")
print(a[0] + " " +  a[1] + " " + a[2])

# 026.
phone_number = "010-1111-2222"
a = phone_number.split("-")
print(a[0] + a[1] + a[2])

# 027.
url = "http://sharebook.kr"
print(url[-2:])

# 028.
lang = 'python'
lang[0] = 'P'
print(lang)
# 문자열은 대입으로 변경 불가
# 리스트로 전환한 후 변경하거나, replace() 사용

# 029.
string = 'abcdfe2a354a32a'
string = string.replace("a", "A")
print(string)

# 030.
string = 'abcd'
string.replace('b', 'B')
print(string)
# string을 replace 한 것을 변수에 저장하지 않았으므로,
# 변경하기 전 상태로 출력된다.

# 031.
a = "3"
b = "4"
print(a + b)
# 출력 결과 : "34"

# 032.
print("Hi" * 3)
# 출력 결과 : "HiHiHi"

# 033.
print("-" * 80)

# 034.
t1 = "python"
t2 = "java"
print((t1 + " " + t2 + " ") * 4)

# 035.
name1 = "김민수" 
age1 = 10
name2 = "이철희"
age2 = 13

print("이름 : %s 나이 : %d" %(name1, age1))
print("이름 : %s 나이 : %d" %(name2, age2))

# 036.
name1 = "김민수" 
age1 = 10
name2 = "이철희"
age2 = 13

print("이름 : {:s} 나이 : {:d}".format(name1, age1))
print("이름 : {:s} 나이 : {:d}".format(name2, age2))

# 037.
name1 = "김민수" 
age1 = 10
name2 = "이철희"
age2 = 13

print(f"이름 : {name1} 나이 : {age1}")
print(f"이름 : {name2} 나이 : {age2}")

# 038.
상장주식수 = "5,969,782,550"
num_list = 상장주식수.split(",")
num = int(num_list[0] + num_list[1] + num_list[2] + num_list[3])
print(num, type(num))

# 039.
분기 = "2020/03(E) (IFRS연결)"
print(분기[:7])

# 040.
data = "   삼성전자    "
data = list(data)
data = data[3:7]
data = data[0] + data[1] + data[2] + data[3]
print(data)

# 041.
ticker = "btc_krw"
upper_ticker = ticker.upper()
print(upper_ticker)

# 042.
ticker = "BTC_KRW"
lower_ticker = ticker.lower()
print(lower_ticker)

# 043.
string = "hello"
string = string.capitalize()
print(string)

# 044.
file_name = "보고서.xlsx"
print(file_name.endswith("xlsx"))

# 045.
file_name = "보고서.xlsx"
print(file_name.endswith(("xlsx", "xls")))

# 046.
file_name = "2020_보고서.xlsx"
print(file_name.startswith("2020"))

# 047.
a = "hello world"
print(a.split())

# 048.
ticker = "btc_krw"
print(ticker.split("_"))

# 049.
date = "2020-05-01"
year, month, day = date.split("-")
print("연도 : {0}, 월 : {1}, 일 : {2}".format(year, month, day))

# 050.
data = "039490     "
data = list(data[:6])
data = data[0] + data[1] + data[2] + data[3] + data[4] + data[5]
print(data)

# 051.
movie_rank = ["닥터 스트레인지", "스플릿", "럭키"]
print(movie_rank)

# 052.
movie_rank = ["닥터 스트레인지", "스플릿", "럭키"]
movie_rank.append("배트맨")
print(movie_rank)

# 053.
movie_rank = ['닥터 스트레인지', '스플릿', '럭키', '배트맨']
movie_rank.insert(1, "슈퍼맨")
print(movie_rank)

# 054.
movie_rank = ['닥터 스트레인지', '슈퍼맨', '스플릿', '럭키', '배트맨']
del movie_rank[3]
print(movie_rank)

# 055.
movie_rank = ['닥터 스트레인지', '슈퍼맨', '스플릿', '배트맨']
del movie_rank[-1]; del movie_rank[-1]
print(movie_rank)

# 056.
lang1 = ["C", "C++", "JAVA"]
lang2 = ["Python", "Go", "C#"]
lang = lang1 + lang2
print(lang)

# 057.
nums = [1, 2, 3, 4, 5, 6, 7]
print("max : {0}".format(max(nums)))
print("min : {0}".format(min(nums)))

# 058.
nums = [1, 2, 3, 4, 5]
print(sum(nums))

# 059.
cook = ["피자", "김밥", "만두", "양념치킨", "족발", "피자", "김치만두", "쫄면", "소시지", "라면", "팥빙수", "김치전"]
print(len(cook))

# 060.
nums = [1, 2, 3, 4, 5]
print(sum(nums) / len(nums))

# 061.
price = ['20180728', 100, 130, 140, 150, 160, 170]
print(price[1:])

# 062.
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(nums[::2])

# 063.
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(nums[1::2])

# 064.
nums = [1, 2, 3, 4, 5]
print(nums[::-1])

# 065.
interest = ['삼성전자', 'LG전자', 'Naver']
print(interest[0] + " " + interest[2])

# 066.
interest = ['삼성전자', 'LG전자', 'Naver', 'SK하이닉스', '미래에셋대우']
print(" ".join(interest))

# 067.
interest = ['삼성전자', 'LG전자', 'Naver', 'SK하이닉스', '미래에셋대우']
print("/".join(interest))

# 068.
interest = ['삼성전자', 'LG전자', 'Naver', 'SK하이닉스', '미래에셋대우']
print("\n".join(interest))

# 069.
string = "삼성전자/LG전자/Naver"
interest = string.split("/")
print(interest)

# 070.
data = [2, 4, 3, 1, 5, 10, 9]
print(sorted(data))

# 071.
my_variable = ()
print(type(my_variable))

# 072.
movie_rank = "닥터 스트레인지", "스플릿", "럭키"
print(movie_rank, type(movie_rank))

# 073.
num = 1,
print(num, type(num))

# 074.
t = (1, 2, 3)
t[0] = 'a'
# 튜플은 리스트와 달리 원소 값을 변경할 수 없다. 변경하려면 리스트로 전환 후 변경 해준다.

# 075.
t = 1, 2, 3, 4
print(t, type(t))
# 튜플 데이터 타입이다.

# 076.
t = ('a', 'b', 'c')
t = list(t)
t[0] = "A"
t = tuple(t)
print(t, type(t))

# 077.
interest = ('삼성전자', 'LG전자', 'SK Hynix')
interest = list(interest)
print(interest, type(interest))

# 078.
interest = ['삼성전자', 'LG전자', 'SK Hynix']
interest = tuple(interest)
print(interest, type(interest))

# 079.
temp = ('apple', 'banana', 'cake')
a, b, c = temp
print(a, b, c)
# 실행 결과 : apple banana cake

# 080.
even = tuple(range(2, 100, 2))
print(even)