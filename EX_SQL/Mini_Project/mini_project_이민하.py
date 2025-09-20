import pymysql
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm, rc


def input_sql(query):
    conn = pymysql.connect(host = 'localhost', user = 'root', password = '1234',
                       db = 'mini_project', charset = 'utf8')

    cur = conn.cursor()

    cur.execute(query)

    rows = cur.fetchall()
    data = pd.DataFrame(rows)


    L = []
    desc = cur.description
    for i in range(len(desc)):
        L.append(desc[i][0])

    data.columns = L

    cur.close()
    conn.close()

    return data

font_path = r"C:\Users\KDP-2\OneDrive\바탕 화면\Python\EX_PANDAS06\DAY_07\MALGUN.TTF"
# 폰트 패밀리 이름 가져오기
font_name = fm.FontProperties(fname = font_path).get_name()
# 새로운 폰트 패밀리 이름 지정
rc('font', family = font_name)

query = """
select g.Country as Country, g.Year_2024 as gdp, m.Cigarettes_20_Pack as Cigarette_Price, 
t.total_tax as Tax_rate, r.ranking as gdp_ranking, p.Cost_of_Living_Index as Cost_of_living
from gdp_data as g
    inner join marlboro_data as m
    on g.Country = m.Country
    inner join raise_taxes as t
    on m.Country = t.Country
    inner join 2024_gdp_ranking as r
    on g.Country = r.Country
    inner join price_ranking as p
    on m.Country = p.Country
"""

data = input_sql(query)

data["gdp"].replace("n/a", np.nan, inplace = True)
data["gdp"] = data["gdp"].astype(str).str.replace(",", "")
data["gdp"] = data["gdp"].astype("float64")
data["Cigarette_Price"] = data["Cigarette_Price"].astype("float64")
data["Tax_rate"] = data["Tax_rate"].astype(str).str.replace("%", "")
data["Tax_rate"] = data["Tax_rate"].astype("float64")

print(data.info())

print(data.head())

data = data.sort_values('gdp_ranking')
print(data.head(10))

sorted_data = data.sort_values('Tax_rate', ascending = False)
print(sorted_data.head(10))

colors = plt.cm.tab20.colors

fig = plt.figure()
axes = fig.subplots(1, 2)
axes[0].bar(data.head(10)['Country'], data.head(10)['gdp'], color = colors[:10], label = data.head(10)['Country'])
axes[0].set_xticklabels(data.head(10)['Country'], rotation = 70)
axes[0].set_title('GDP')
axes[0].legend()
axes[0].set_xlabel('Country')
axes[0].set_ylabel('GDP (Billion $)')
data = data.sort_values('Cigarette_Price', ascending = False)
axes[1].bar(data.head(10)['Country'], data.head(10)['Cigarette_Price'], color = colors[:10], label = data.head(10)['Country'])
axes[1].set_xticklabels(data.head(10)['Country'], rotation = 70)
axes[1].set_title('Cigarette_Price')
axes[1].legend()
axes[1].set_xlabel('Country')
axes[1].set_ylabel('Cigarette price (1 pack)')
plt.tight_layout()
plt.suptitle("GDP와 말보로 가격 상위 10개국", size = 16)
plt.show()


data = data.sort_values('Cigarette_Price', ascending = False)
fig = plt.figure()
axes = fig.subplots(1, 2)
axes[0].bar(data.head(10)['Country'], data.head(10)['Cigarette_Price'], color = colors[:10], label = data.head(10)['Country'])
axes[0].set_xticklabels(data.head(10)['Country'], rotation = 70)
axes[0].set_title('Cigarette Price')
axes[0].legend()
axes[0].set_xlabel('Country')
axes[0].set_ylabel('Cigarette price (1 pack)')

sorted_data = data.sort_values('Tax_rate', ascending = False)
axes[1].bar(sorted_data.head(10)['Country'], sorted_data.head(10)['Tax_rate'], color = colors[:10], label = sorted_data.head(10)['Country'])
axes[1].set_xticklabels(sorted_data.head(10)['Country'], rotation = 70)
axes[1].set_title('Tax_rate (%)')
axes[1].legend()
axes[1].set_xlabel('Country')
axes[1].set_ylabel('tax rate (%)')
plt.tight_layout()
plt.suptitle("말보로 가격과 담배 관세 비율 상위 10개국", size = 16)
plt.show()


data = data.sort_values('gdp', ascending = False)
fig = plt.figure()
axes = fig.subplots(2, 2)
country = ['Australia', 'New Zealand', 'Ireland', 'United Kingdom', 'Korea']
data = data.sort_values('Country')
L = [data[data['Country'] == country[0]].index[0], data[data['Country'] == country[1]].index[0],
     data[data['Country'] == country[2]].index[0],
     data[data['Country'] == country[3]].index[0],
     data[data['Country'] == country[4]].index[0]]
print(L)

data = data.iloc[L]

axes[0][0].bar(data['Country'], data['gdp'], color = colors[:10], label = data['Country'])
axes[0][0].set_xticklabels(data.head(10)['Country'], size = 5)
axes[0][0].set_title('GDP 5개국')
axes[0][0].set_xlabel('Country')
axes[0][0].set_ylabel('GDP (Billion $)')
axes[0][0].legend()

data = data.sort_values('Cigarette_Price', ascending = False)
axes[0][1].bar(data.head(10)['Country'], data.head(10)['Cigarette_Price'], color = colors[:10], label = data.head(10)['Country'])
axes[0][1].set_xticklabels(data.head(10)['Country'], size = 5)
axes[0][1].set_title('말보로 담배 가격 5개국')
axes[0][1].set_xlabel('Country')
axes[0][1].set_ylabel('Cigarette price (1 pack)')
axes[0][1].legend()

data = data.sort_values('Tax_rate', ascending = False)
axes[1][0].bar(data.head(10)['Country'], data.head(10)['Tax_rate'], color = colors[:10], label = data.head(10)['Country'])
axes[1][0].set_xticklabels(data.head(10)['Country'], size = 5)
axes[1][0].set_title('담배 관세 비율 5개국')
axes[1][0].set_xlabel('Country')
axes[1][0].set_ylabel('tax rate (%)')
axes[1][0].legend()


data = data.sort_values('Cost_of_living', ascending = False)
axes[1][1].bar(data.head(10)['Country'], data.head(10)['Cost_of_living'], color = colors[:10], label = data.head(10)['Country'])
axes[1][1].set_xticklabels(data.head(10)['Country'], size = 5)
axes[1][1].set_title('생계비 지수 5개국')
axes[1][1].set_xlabel('Country')
axes[1][1].set_ylabel('Cost_of_living')
axes[1][1].legend()


plt.suptitle("종합 비교", size = 16)
plt.show()