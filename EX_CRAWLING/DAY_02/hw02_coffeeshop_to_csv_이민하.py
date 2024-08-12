from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

def make_dataframe():
    index = 1
    
    store_list = []

    for num in range(1, 51):
        url = f'https://www.hollys.co.kr/store/korea/korStore2.do?pageNo={num}&sido=&gugun=&store='
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        list = soup.select('tr')    


        for i in range(1, len(list)):
            
            area = list[i].select('td.center_t')[0].text
            name = list[i].select('td.center_t')[1].text
            address = list[i].select('td.center_t')[3].text
            number = list[i].select('td.center_t')[5].text

            store_list.append([area, name, address, number])
            print(f"[{index:3}] : 매장이름 : {name}, 지역 : {area}, 주소 : {address}, 전화번호 : {number}")          
            index += 1

    data = pd.DataFrame(store_list)
    data.columns = ["지역", "매장이름", "주소", "전화번호"]
    data.to_csv('hollys_branches.csv')

    print(f"전체 매장 수 : {len(data)}")
    print("hollys_branches.csv 파일 저장 완료")
    return data

make_dataframe()
