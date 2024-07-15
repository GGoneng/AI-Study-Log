# [18.5] continue
# 0 ~ 73 사이의 숫자 중 3으로 끝나는 숫자 출력

i = 0
while True:
   
    if i > 72: break
    i += 1
    if i % 10 != 3: continue
    print(i, end = " ")
    