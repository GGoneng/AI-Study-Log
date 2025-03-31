import csv

f = open("subwayfee.csv", encoding = "utf-8-sig")
data = csv.reader(f)
header = next(data)
rate = 0

for row in data:
    for i in range(4, 8):
        row[i] = int(row[i])
    rate = row[4] / (row[4] + row[6])

    if row[6] == 0:
        print(row)

    print(rate)
f.close()