'''
데이터 크롤링과 정제 과제 #2: 커피 매장 찾기

- https://www.hollys.co.kr

- 매장 찾기 페이지 url
 https://www.hollys.co.kr/store/korea/korStore2.do?pageNo=1&sido=&gugun=&store=
  - pageNo=1 ~ pageNo=50까지 모두 검색
  - 크롤링한 정보는 csv 파일로 저장함
   . list -> Pandas.DataFrame -> csv 파일 저장

'''

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import csv
import collections

collections.Callable = collections.abc.Callable

branches = [] # 커피 매장 저장 리스트
end_page = 50 # 커피 매장 마지막 페이지: 50
index = 1

for page in range(1, end_page+1):
    hollys_url = 'https://www.hollys.co.kr/store/korea/korStore2.do?pageNo={0}&sido=&gugun=&store='.format(page)

    html = urlopen(hollys_url)
    soup = BeautifulSoup(html, 'html.parser')
    tag_tbody = soup.find('tbody')

    for store in tag_tbody.find_all('tr'):
        store_td = store.find_all('td')
        store_city = store_td[0].string     # 매장이 있는 지역(시, 구)
        store_name = store_td[1].string     # 매장 이름
        store_address = store_td[3].string  # 매장 주소
        store_phone = store_td[5].string    # 매장 전화번호

        print(f'[{index:3d}]: 매장이름: {store_name}, 지역: {store_city}, '
              f'주소: {store_address}, 전화번호: {store_phone}')

        branches.append([store_name, store_city, store_address, store_phone])
        index += 1

print(f'전체 매장 수: {len(branches)}')

#
# 크롤링한 데이터를 CSV 파일로 저장하기
# 리스트를 pandas dataframe으로 변경 -> csv 파일로 저장
#
# 방법 #1

file_name = 'hollys_branches.csv'

hollys_table = pd.DataFrame(branches, columns=('매장이름', '지역', '주소', '전화번호'))

# utf-8로 인코딩
hollys_table.to_csv('hollys_branches.csv',
                    encoding='utf-8', mode='w', index=True)


# 방법 2
# csv 모듈 사용: import csv
'''
file_name = 'hollys_branches.csv'
f = open(file_name, 'w', encoding='utf-8', newline='')
csv_writer = csv.writer(f)

header_list=['매장이름', '지역', '주소', '전화번호']
csv_writer.writerow(header_list)
for branch in branches:
    csv_writer.writerow(branch)

f.close()

print(f'{file_name} 파일 저장 완료')
'''