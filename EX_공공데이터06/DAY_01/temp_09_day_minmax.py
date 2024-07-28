import csv
import matplotlib.pyplot as plt
import platform
import koreanize_matplotlib


def draw_lowhigh_graph(start_year, month, day):
    f = open('daegu-utf8.csv', encoding = 'utf-8-sig')
    data = csv.reader(f)
    next(data)
    high_temp = []
    low_temp = []
    x_year = []

    for row in data:
        if row[-1] != '':
            date_string = row[0].split('-')
            if int(date_string[0]) >= start_year:
                if int(date_string[1]) == month and int(date_string[2]) == day:
                    high_temp.append(float(row[-1]))
                    low_temp.append(float(row[-2]))
                    x_year.append(date_string[0])

    plt.figure(figsize = (20, 4))
    plt.plot(x_year, high_temp, 'hotpink', marker = "o", label = "최고기온")
    plt.plot(x_year, low_temp, 'royalblue', marker = 's', label = '최저기온')

    plt.rcParams["axes.unicode_minus"] = False
    plt.title(F"{start_year}년 이후 {month}월 {day}일의 온도 변화 그래프", size = 16)

    plt.legend(loc = 2)
    plt.xlabel("year")
    plt.ylabel("temperature")
    plt.show()

def main():
    draw_lowhigh_graph(2000, 5, 12)

main()