dan = int(input("출력 원하는 단 입력 : "))

for i in range(2, 10):
    print(F"\n[{i}단] ",end = '  ')
    for j in range(1, 10):
        print(F"{i} * {j} = {i * j}", end = "\t")
        if j == i:
            break 
    if i == dan: break

for i in range(2, dan + 1):
    print(F"\n[{i}단] ", end = "  ")
    for j in range(1, i + 1):
        print(F"{i} * {j} = {i * j}", end = "\t")
