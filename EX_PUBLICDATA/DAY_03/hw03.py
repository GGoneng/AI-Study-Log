import csv
import matplotlib.pyplot as plt
import koreanize_matplotlib
import re

def draw_gender_population(city, title, male_num_list, female_num_list):
    fig = plt.figure(figsize = (8, 12))
    axes = fig.subplots(5, 2)
    for i in range(5):
        for j in range(2):
            axes[i, j].pie([male_num_list[i * 2 + j], female_num_list[i * 2 + j]], autopct = "%.1f%%", 
                           startangle = 90, textprops = {"fontsize" : 8}, labels = ["남성", "여성"])
            axes[i, j].set_title(city[i * 2 + j], size = 8)
    plt.suptitle(title, size = 20)
    plt.show()

def get_city_name(city):
    city_name = re.split("[()]", city)
    return city_name[0]

def print_population(titles, male, female):
    for i in range(len(titles)):
        print(f"{titles[i].strip()} : (남:{male[i]:,} 여:{female[i]:,})")

def get_gender_population(city):
    with open("gender.csv", encoding = "euc_kr") as f:
        data = csv.reader(f)
        header = next(data)

        male = []
        female = []
        titles = []

        for row in data:
            if city in row[0]:
                male.append(int(row[104].replace(",", "")))
                female.append(int(row[207].replace(",", "")))
                titles.append(get_city_name(row[0]))
                
        print_population(titles, male, female)
        draw_gender_population(titles, city + " 구별 남녀 인구 비율", male, female)

get_gender_population("대구광역시")