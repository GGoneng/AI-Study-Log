L = []
count = 0
row, col = map(int, input().split())

for i in range(row):
    L.append(list(input()))

for i in range(row):
    for j in range(col):    
        if L[i][j] == ".":
            for k in range(-1, 2, 1):
                for l in range(-1, 2, 1):
                    if (i + k) < 0 or (j + l) < 0 or (i + k) >= row or (j + l) >= col :
                            continue
                    if L[i + k][j + l] == "*": 
                        count += 1
                        
            L[i][j] = count
            count = 0 

for i in range(row):
    for j in range(col):
        print(L[i][j], end = "")
    print()

