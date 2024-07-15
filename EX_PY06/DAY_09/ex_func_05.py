"""
함수명에 대해서
-> 코드가 있는 부분에 붙여진 이름
-> 코드가 시작되는 주소를 저장하고 있음
"""

# [내장함수]
show = print

show("Happy")

datas = [11, 22, 33]
func = [max, min, sum]

print(func[0](datas), func[1](datas), func[2](datas))