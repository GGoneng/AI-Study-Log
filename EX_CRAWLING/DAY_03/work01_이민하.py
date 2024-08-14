import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

def open_html(url):
    html = requests.get(url)
    bs = BeautifulSoup(html.text, 'html.parser')

    return bs

def extract_url_name(bs):
    search = bs.find('tbody')
    search_results = search.find_all('a', {'class' : 'tltle'})
    search_results = search_results[:10]

    top_10_list = []
    url_list = []
    code_list = []

    for name in search_results:
        top_10_list.append(name.text)
        url_list.append("https://finance.naver.com" + name.attrs['href'])
        code_list.append(name.attrs['href'][22:])

    return top_10_list, url_list, code_list

def extract_price(code_list):
    now = []
    yesterday = []
    market_price = []
    high = []
    low = []


    for code in code_list:
        url = "https://finance.naver.com/item/main.naver?code=" + code
        html = requests.get(url)
        bs = BeautifulSoup(html.text, 'html.parser')
        
        search = bs.find('body')
        search_results = search.find('dl', {'class' : 'blind'})
        price_results = search_results.find_all('dd')
        now.append(int(price_results[3].text[4:11].strip().replace(",", "")))
        yesterday.append(int(price_results[4].text[4:].replace(",", "")))
        market_price.append(int(price_results[5].text[3:].replace(",", "")))
        high.append(int(price_results[6].text[3:].replace(",", "")))
        low.append(int(price_results[8].text[3:].replace(",", "")))
    
    return now, yesterday, market_price, high, low

def print_enterprise_list(top_10_list):
    print('-' * 40)
    print("[ 네이버 코스피 상위 10위 기업 목록 ]")
    print('-' * 40)

    for idx, enterprise in enumerate(top_10_list):
        print(f"[{idx + 1 :2d}] {enterprise}")

def get_idx():
    idx = int(input("추가로 검색할 기업의 번호를 입력하세요(-1: 종료) : "))
    return idx

def print_price(top_10_list, code_list, now, yesterday, market_price, high, low, idx):
    print(f"종목명 : {top_10_list[idx - 1]}")
    print(f"종목코드 : {code_list[idx - 1]}")
    print(f"현재가 : {now[idx - 1]:,}")
    print(f"전일가 : {yesterday[idx - 1]:,}")
    print(f"시가 : {market_price[idx - 1]:,}")
    print(f"고가 : {high[idx - 1]:,}")
    print(f"저가 : {low[idx - 1]:,}")

def main():
    url = 'https://finance.naver.com/sise/sise_market_sum.naver'
    
    bs = open_html(url)
    top_10_list, url_list, code_list = extract_url_name(bs)
    now, yesterday, market_price, high, low = extract_price(code_list)
    
    while True:
        print_enterprise_list(top_10_list)   
        idx = get_idx()
    
        if idx == -1:
            break
        print(url_list[idx - 1])
        print_price(top_10_list, code_list, now, yesterday, market_price, high, low, idx)
        
main()