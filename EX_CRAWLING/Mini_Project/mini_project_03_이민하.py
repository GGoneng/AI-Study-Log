from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from konlpy.tag import Okt
import platform
import numpy as np
from PIL import Image
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def url_open(url):
    urlrequest = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(urlrequest)

    return html

def make_enterprise_list(html):
    soup = BeautifulSoup(html, 'html.parser')
    soup2 = soup.find_all('div', {'class' : 'item_recruit'})
    enterprise_list = []
    
    for enterprise in soup2:
        enterprise_list.append('https://www.saramin.co.kr' + enterprise.find('a', {'class' : 'data_layer'}).attrs['href'])
        
    return enterprise_list

def crawling(url_list, driver):

    info = ""
    for url in url_list:    
        try:
            driver.get(url)    
            driver.switch_to.frame('iframe_content_0')

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            soup2 = soup.find_all('span')
            for information in soup2:
                info += (information.text)
        except Exception as e:
            continue           
    return info

def info_pos(text, list):
    okt = Okt()

    okt_pos = okt.pos(text, norm = True, stem = True)
    for word, tag in okt_pos:
        if (tag in ['Alpha']) and (word.find('m') < 0) and (word.find('AI') < 0) and (word.find('IT') < 0):
            list.append(word)
    print(len(list))
    return list

def make_wordcloud(list):
    counts = Counter(list)
    tags = counts.most_common(50)
    
    if platform.system() == 'Windows':
        path = r'c:\Windows\Fonts\malgun.ttf'
    elif platform.system() == 'Darwin':
        path = r'/System/Library/Fonts/AppleGothic'
    else:
        font = r'/usr/share/fonts/truetype/name/NanumMyeongjo.ttf'
    
    img_mask = np.array(Image.open('book.jpg'))
    wc = WordCloud(font_path = path, width = 400, height = 400,
                   background_color = 'white', max_font_size = 200,
                   repeat = True, colormap = 'inferno', mask = img_mask)

    cloud = wc.generate_from_frequencies(dict(tags))
    plt.figure(figsize = (10, 8))
    plt.axis('off')
    plt.imshow(cloud)
    plt.show()

def main():
    info_list = []
    driver = webdriver.Chrome()

    for i in range(1, 6):
        url = f"https://www.saramin.co.kr/zf_user/search?searchType=search&searchword=%EB%8D%B0%EC%9D%B4%ED%84%B0+%EB%B6%84%EC%84%9D%EA%B0%80&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9%2C10&keydownAccess=&panel_type=&search_optional_item=y&search_done=y&panel_count=y&preview=y&recruitPage={i}&recruitSort=relation&recruitPageCount=100&inner_com_type=&show_applied=&quick_apply=&except_read=&ai_head_hunting=&mainSearch=y"
        html = url_open(url)
        enterprise_list = make_enterprise_list(html)
        info_text = crawling(enterprise_list, driver)
        info_list = info_pos(info_text, info_list)
    print(len(info_list))
    make_wordcloud(info_list)

main()