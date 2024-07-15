# 1번 문제
dan = 2
idx = 9

for i in range(0, 72):
    print(F"{dan} * {(i % idx) + 1} = {dan * ((i % idx) + 1)}")
    if (i + 1) % idx == 0:
        dan += 1
        print()

# 2번 문제
for i in range(1, 10):
    for j in range(2, 6):
        print(F"{j} * {i} = {i * j}", end = "\t")
    print()

print()

for i in range(1, 10):
    for j in range(6, 10):
        print(F"{j} * {i} = {j * i}", end = "\t")
    print()