from urllib.request import urlopen
from bs4 import BeautifulSoup




def scraping_use_find(html):
    container = html.find_all('div', {'class': 'tombstone-container'})
    print("[find 함수 사용]")
    print(f"총 tomestone-container 검색 개수 : {len(container)}")
    for c1 in container:
        print("------------------------------------------------------")    
        print(f"[Period] : {c1.find('p', {'class' : 'period-name'}).text}")
        print(f"[Short desc] : {c1.find('p', {'class' : 'short-desc'}).text}")
        print(f"[Temperature] : {c1.find_all('p')[2].text}")
        print(f"[Image desc] : {c1.find('img')['title']}")
        print()

def scraping_use_select(html):
    container = html.select('div.tombstone-container')  
    print("[select 함수 사용]")
    print(F"총 tomestone-conatiner 검색 개수 : {len(container)}")

    for c1 in container:
        print('------------------------------------------------------')
        print(f"[Period] : {c1.select_one('p.period-name').text}")
        print(f"[Short desc] : {c1.select_one('p.short-desc').text}")
        print(f"[Temperature] : {c1.select('p')[2].text}")
        print(f"[Image desc] : {c1.select_one('img')['title']}")
        print()


def main():

    url = 'https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168#.Yst5ji9yxTY'
    html = urlopen(url)
    bs = BeautifulSoup(html.read(), 'html.parser')

    scraping_use_find(bs) 
    scraping_use_select(bs)
main()