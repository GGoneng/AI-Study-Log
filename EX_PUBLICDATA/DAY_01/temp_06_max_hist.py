import csv
import matplotlib.pyplot as plt
import koreanize_matplotlib

f = open("daegu-utf8.csv", encoding = "utf-8-sig")
data = csv.reader(f)
next(data)
result = []

for row in data:
    if row[-1] != "":
        result.append(float(row[-1]))
f.close()

plt.figure(figsize = (10, 2))
plt.hist(result, bins = 500, color = "blue")

plt.rcParams["axes.unicode_minus"] = False
plt.title("1907년 부터 2024년까지 대구 기온 히스토그램")
plt.show()