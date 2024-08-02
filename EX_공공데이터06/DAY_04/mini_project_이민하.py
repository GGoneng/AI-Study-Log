import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import koreanize_matplotlib

def north_temperature():
    data = pd.read_csv("data2.csv", encoding = "euc_kr")
    data.columns = ["year", "area", "mean_temperature", "mean_min_temperature", "mean_max_temperature"]
    data.dropna(axis = 0, inplace = True)
    data["year"] = data["year"].astype("int64")
    plt.figure()
    plt.plot(data["year"], data["mean_temperature"], label = "북강릉", linewidth = 2)

    data2 = pd.read_csv("data4.csv", encoding = "euc_kr")
    data2.columns = ["year", "area", "mean_temperature", "mean_min_temperature", "mean_max_temperature"]
    data2.dropna(axis = 0, inplace = True)
    data2["year"] = data2["year"].astype("int64")
    plt.plot(data2["year"], data2["mean_temperature"], label = "서울", linewidth = 2)
    z = np.polyfit(data2["year"], data2["mean_temperature"], 1)
    p = np.poly1d(z)
    print(p(data2["year"]))
    plt.plot(data2["year"], p(data2["year"]), linestyle="--", color="grey", label = round(1 - (p(data2["year"]) / 20)[2], 2))

    plt.tight_layout()    
    plt.ylim(9, 16)
    plt.legend()
    plt.ylabel("기온(℃)")
    plt.xlabel("연도")
    plt.title("중부 지방의 기온 차", size = 15)
    plt.show()


def south_temperature():
    data = pd.read_csv("data3.csv", encoding = "euc_kr")
    data.columns = ["year", "area", "mean_temperature", "mean_min_temperature", "mean_max_temperature"]
    data.dropna(axis = 0, inplace = True)
    data["year"] = data["year"].astype("int64")
    plt.figure()
    plt.plot(data["year"], data["mean_temperature"], label = "대구", linewidth = 2)

    data2 = pd.read_csv("data5.csv", encoding = "euc_kr")
    data2.columns = ["year", "area", "mean_temperature", "mean_min_temperature", "mean_max_temperature"]
    data2.dropna(axis = 0, inplace = True)
    data2["year"] = data2["year"].astype("int64")
    plt.plot(data2["year"], data2["mean_temperature"], label = "부산", linewidth = 2)
    z = np.polyfit(data["year"], data["mean_temperature"], 1)
    p = np.poly1d(z)
    print(p(data["year"]))
    plt.plot(data["year"], p(data["year"]), linestyle="--", color="grey" , label = round(1 - (p(data["year"]) / 20)[2], 2))


    plt.tight_layout()    
    plt.ylim(9, 16)
    plt.legend()
    plt.ylabel("기온(℃)")
    plt.xlabel("연도")
    plt.title("남부 지방의 기온 차", size = 15)
    plt.show()



def distract_data(data, area, thing, option, null_list):
    distracted = data[data[("지점", "Unnamed: 0_level_1")] == area][(thing, option)]
    distracted.replace(null_list, np.nan, inplace = True)

    distracted.dropna(inplace = True)
    distracted = pd.to_datetime(distracted)

    return distracted

def get_xticks(before_data, area):
    x_ticks_list = before_data[before_data[("지점", "Unnamed: 0_level_1")] == area][("년도", "Unnamed: 1_level_1")]
    return x_ticks_list

def draw_plot(fig, data, distracted_data, area, color):
    L = get_xticks(data, area)

    Y = []
    for i in range(3):
        Y.append(f"{i + 3}월")

    Y2 = []
    for i in range(3):
        Y2.append((i + 3) * 30)

    z = np.polyfit(distracted_data.dt.year, distracted_data.dt.month * 30 + distracted_data.dt.day, 1)
    p = np.poly1d(z)
    fig.plot(distracted_data.dt.year, p(distracted_data.dt.year), linestyle="--", color="grey")

    fig.plot(distracted_data.dt.year, distracted_data.dt.month * 30 + distracted_data.dt.day, color = color, marker = "o", markersize = 3, linewidth = 2)
    fig.grid(True, linewidth = 0.5)
    fig.set_xlabel("연도")
    fig.set_ylabel("기온(℃)")
    fig.set_title(area)
    fig.set_xticks(L, L, rotation = 70)
    fig.set_yticks(Y2, Y)


def main():

    data = pd.read_csv("data.csv", header = [0, 1] ,encoding = "euc_kr")
    print(data.info())

    null_list = ["관측 안됨", "―", " ", "관측 중지", "결측"]
    butterfly_area_list = ["서울", "북강릉", "대전", "전주", "대구", "부산"]
    color_list = ["purple", "tomato", "pink", "lightgreen", "royalblue", "green"]

    north_temperature()
    south_temperature()
    
    fig = plt.figure()
    axes = fig.subplots(3, 2, sharex = True)
    for i in range(3):
        for j in range(2):
            draw_plot(axes[i, j], data, distract_data(data, butterfly_area_list[i * 2 + j], "나비", "초견", null_list), butterfly_area_list[i * 2 + j], color_list[i * 2 + j])
    plt.tight_layout()
    plt.suptitle("나비의 초견 시기", size = 20)
    plt.show()


    fig = plt.figure()
    axes = fig.subplots(3, 2, sharex = True)
    for i in range(3):
        for j in range(2):
            draw_plot(axes[i, j], data, distract_data(data, butterfly_area_list[i * 2 + j], "개나리", "개화", null_list), butterfly_area_list[i * 2 + j], color_list[i * 2 + j])
    plt.tight_layout()
    plt.suptitle("개나리의 개화 시기", size = 20)
    plt.show()


    fig = plt.figure()
    axes = fig.subplots(3, 2, sharex = True)
    for i in range(3):
        for j in range(2):
            draw_plot(axes[i, j], data, distract_data(data, butterfly_area_list[i * 2 + j], "벚나무", "개화", null_list), butterfly_area_list[i * 2 + j], color_list[i * 2 + j])
    plt.tight_layout()
    plt.suptitle("벚나무의 개화 시기", size = 20)
    plt.show()



main()