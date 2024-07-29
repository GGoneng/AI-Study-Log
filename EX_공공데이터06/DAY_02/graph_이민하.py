import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

df = pd.read_excel("subway.xls", sheet_name = "지하철 시간대별 이용현황", header = [0, 1])
print(df.head())

people_list = []
station_list = []

print(df.columns)
print(df[('호선명', 'Unnamed: 1_level_1')])
print(df[("지하철역", "Unnamed: 3_level_1")])

commute_time_df = df.iloc[:, [11, 13]]
commute_time_df[("07:00:00~07:59:59", "하차")] = commute_time_df[("07:00:00~07:59:59", "하차")].apply(lambda x : x.replace(",", ""))
commute_time_df[("08:00:00~08:59:59", "하차")] = commute_time_df[("08:00:00~08:59:59", "하차")].apply(lambda x : x.replace(",", ""))

commute_time_df = commute_time_df.astype({("07:00:00~07:59:59", "하차"):"int64"})
commute_time_df = commute_time_df.astype({("08:00:00~08:59:59", "하차"):"int64"})

for i in range(7):
    max_number = commute_time_df[df[('호선명', 'Unnamed: 1_level_1')] == f"{i + 1}" + "호선"].sum(axis = 1).max()
    max_index = commute_time_df[df[('호선명', 'Unnamed: 1_level_1')] == f"{i + 1}" + "호선"].sum(axis = 1).idxmax()
    
    max_line, max_station = df.iloc[max_index, [1, 3]]

    print(F"출근 시간대 {max_line} 최대 하차역 : {max_station}역, 하차인원 : {max_number:,}명")

    people_list.append(max_number)
    station_list.append(f"{max_line} {max_station}")

plt.figure(figsize = (12, 8))
plt.bar(range(7), people_list)
plt.xticks(range(7), station_list, rotation = 80)
plt.title("출근 시간대 지하철 노선별 최대 하차 인원 및 하차역")
plt.show()