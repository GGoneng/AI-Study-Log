"""
대구 기온 데이터에서 시작 연도, 마지막 연도를 입력하고 특정 월의 최고 기온 및 최저 기온의 평균값을 구하고 그래프로 표현
입력 받을 값 : 시작 연도, 마지막 연도, 특정 월
최고 기온, 최저 기온 구하기
날짜 데이터 => datetime 형태로 바꾸기
함수 매개변수 필요없음
"""

import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

data = pd.read_csv('daegu-utf8-df.csv', encoding = "utf-8-sig")

print(data.columns)

def draw_graph(title, x_list, list1, list1_label, list2, list2_label):
    plt.figure(figsize = (15, 5))
    plt.plot(x_list, list1, color = "red", marker = 's', label = list1_label)
    plt.plot(x_list, list2, color = "blue", marker = 's', label = list2_label)
    plt.title(title)
    plt.xticks(x_list)
    plt.legend(loc = 2)
    plt.show()

def main():

    max_temp = []
    min_temp = []
    year_list = []
    
    data["날짜"] = pd.to_datetime(data["날짜"], format = "%Y-%m-%d")
 
    start_year = int(input("시작 연도를 입력하세요 : "))
    end_year = int(input("마지막 연도를 입력하세요 : "))
    input_month = int(input("기온 변화를 측정할 달을 입력하세요 : "))


    for i in range(end_year - start_year + 1):
        filtered_year = data[(data["날짜"].dt.month == input_month)  & (data["날짜"].dt.year == start_year + i)]
        max_temp.append(float(round(filtered_year["최고기온"].mean(), 1)))
        min_temp.append(float(round(filtered_year["최저기온"].mean(), 1)))
        year_list.append(start_year + i)

    print(F"{start_year}년부터 {end_year}년까지 {input_month}월의 기온 변화")
    print(f"{input_month}월 최저기온 평균 : ")
    for i in range(len(min_temp)):
        print(F"{min_temp[i]}", end = ", ")

    print(f"\n\n{input_month}월 최고기온 평균 :")
    for i in range(len(max_temp)):
        print(F"{max_temp[i]}", end = ", ")
    
    draw_graph(f"{start_year}년부터 {end_year}년까지 {input_month}월의 기온 변화", year_list, max_temp, "최고기온", min_temp, '최저기온')

main()