# [1] outer = 5, inner = 5
for i in range(5):
    for j in range(5):
        print(F"j : {j}", end = " ")
    print(F"i : {i}\\n")

# [2] 대각선 * 출력
for i in range(5):
    for j in range(i  + 1):
#         if i == j:
#             print("*", end = "")
#         else:
#             print(" ", end = "")
#     print()
        print("*" if j == i else " ", end = "\n" if j == i else '')

# [3] 역삼각형 * 출력

for i in range(5):
    for j in range(5):
        if j >= i:
            print("*", end = "")
        else:
            print(" ", end = "")
    print()