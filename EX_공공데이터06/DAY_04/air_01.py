import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib

dust = pd.read_excel("dust.xlsx")


print(dust.head())
print(tabulate(dust.head(), headers = "keys", tablefmt = "pretty"))

print(dust.info())


dust.rename(columns = {"날짜" : "date", "아황산가스" : "so2", "일산화탄소" : "co",
                       "오존" : "o3", "이산화질소" : "no2"}, inplace = True)


print(tabulate(dust.head(), headers = "keys", tablefmt = "psql"))


dust["date"] = dust["date"].str[:10]
print(tabulate(dust.head(), headers = "keys", tablefmt = "psql"))


dust["date"] = pd.to_datetime(dust["date"])
print(dust.dtypes)


dust["year"] = dust["date"].dt.year
dust["month"] = dust["date"].dt.month
dust["day"] = dust["date"].dt.day
print(dust.columns)


dust = dust[["date", "year", "month", "day", "so2", "co", "o3", "no2", "PM10", "PM2.5"]]
print(dust.columns)


print(" 결측치 개수 확인하기")
print(dust.isna().sum())


print(" 결측치를 포함한 데이터 출력")
print(dust[dust.isna().any(axis = 1)])


print("결측치 채우기")

dust.ffill(inplace = True)
print(dust.isnull().sum())

print(dust.iloc[132:134])


weather = pd.read_excel("weather.xlsx")
print(tabulate(weather.head(), headers = "keys", tablefmt = "psql"))

print(weather.info())


weather.drop(["지점", "지점명"], axis = 1, inplace = True)

weather.columns = ["date", "temp", "wind", "rain", "humidity"]
print(tabulate(weather.head(), headers = "keys", tablefmt = "pretty"))


weather["date"] = pd.to_datetime(weather["date"].dt.date)
print(weather.info())
print(weather.head())


print("날씨 데이터 결측치 개수 확인하기")
print(weather.isna().sum())


print("날씨 데이터에서 결측치를 포함하는 행 출력")
print(weather[weather.isna().any(axis = 1)])


weather.ffill(inplace = True)
print(weather.isna().sum())

print(weather.iloc[[369, 565, 742]])


print("강수량이 0인 항목을 0.01로 변경")
weather["rain"] = weather["rain"].replace(0, 0.01)
print(weather["rain"].value_counts())


print("dust, weather의 크기 확인")
print("dust.shape", dust.shape)
print("weather.shape", weather.shape)


print(dust.iloc[740:])
print(weather.iloc[740:])

dust.drop(index = 743, inplace = True)
print(dust.shape)


print("dust, weather 데이터프레임 merge")

merged_df = pd.merge(dust, weather, on = "date")
print(merged_df.head())
print(merged_df.info())


pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

print(merged_df.corr())


print("미세먼지(PM10)과 상관관계 분석")
corr = merged_df.corr()
print(corr["PM10"].sort_values(ascending = False))


merged_df.hist(column = ["so2", "co", "o3", "no2", "PM10", "PM2.5", "temp", "wind", "rain", "humidity"],
               bins = 50, figsize = (20, 15))
plt.show()


plt.figure(figsize = (15, 10))
daygraph = sns.barplot(x = "day", y = "PM10", data = merged_df)
plt.title("날짜별 PM10 농도")
plt.show()


plt.figure(figsize = (15, 10))
sns.heatmap(data = corr, annot = True, fmt = ".2f", cmap = "hot")
plt.show()


plt.figure(figsize = (15, 10))
x = merged_df["PM10"]
y = merged_df["PM2.5"]


plt.plot(x, y, marker = "o", linestyle = "none", color = "red", alpha = 0.5)
plt.title("PM10 vs. PM2.5")
plt.xlabel("PM10")
plt.ylabel("PM2.5")
plt.show()