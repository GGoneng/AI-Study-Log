import csv

f = open("age.csv", encoding = "euc_kr")
data = csv.reader(f)

header = next(data)

for row in data:
    if "산격3동" in row[0]:
        print(row)

f.close()