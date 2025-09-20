import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import collections
from urllib.request import Request
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from wordcloud import WordCloud
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

if not hasattr(collections,'Callable'):
    collections.Callable = collections.abc.Callable

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome()


name_list = []
# chrome_driver = webdriver.Chrome('chrome/chromedriver', options=chrome_options)
for i in range(50):
    chrome_url = f'https://cafe.naver.com/sqlpd?iframe_url=/ArticleList.nhn%3Fsearch.clubid=21771779%26search.boardtype=L%26search.totalCount=1501%26search.cafeId=21771779%26search.page={i}'
    driver.get(chrome_url)

    driver.switch_to.frame("cafe_main")

    html = driver.page_source
    bs = BeautifulSoup(html, 'html.parser')

    results = bs.find_all('a', {'class':'link_name'})
    
    for name in results:
        name_list.append(name.text)

img_mask = np.array(Image.open('cloud.png'))

wordcloud = WordCloud(width = 400, height = 400,
                      background_color = 'white', max_font_size = 200,
                      stopwords = STOPWORDS,
                      repeat = True,
                      colormap = 'inferno', mask = img_mask).generate(name_list)

print(wordcloud.words_)

plt.figure(figsize = (10, 8))
plt.axis('off')
plt.imshow(wordcloud)
plt.show()