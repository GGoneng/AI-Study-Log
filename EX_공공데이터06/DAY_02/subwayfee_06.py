import csv
max = [0] * 4
max_station = [""] * 4
label = ["유임승차", "유임하차", "무임승차", "무임하차"]

with open("subwayfee.csv", encoding = "utf-8-sig") as f:
    data = csv.reader(f)
    next(data)

    for row in data:
        for i in range(4, 8):
            row[i] = int(row[i])
            if row[i] > max[i - 4]:
                max[i - 4] = row[i]
                max_station[i - 4] = row[3] + " " + row[1]

for i in range(4):
    print(F"{label[i]} : {max_station[i]} {max[i]:,}명")