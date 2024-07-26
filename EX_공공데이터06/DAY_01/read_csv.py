import csv

f = open('daegu.csv', 'r', encoding = 'utf-8')
data = csv.reader(f, delimiter = ",")
count = 0

for row in data:
    if count > 5:
        break
    else:
        print(row)
    count += 1

f.close()