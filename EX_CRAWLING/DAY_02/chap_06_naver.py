from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

query = 'ChatGpt'
query1 = quote('챗지피티')
url = f'https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query={query1}'

html = urlopen(url)
soup = BeautifulSoup(html.read(), 'html.parser')
blog_results = soup.select('a.title_link')
print('검색 결과 수 : ',len(blog_results))

for blog_title in blog_results:
    title = blog_title.text
    link = blog_title['href']
    print(f'{title}, [{link}]')
search_count = len(blog_results)

desc_results = soup.select('a.dsc_link')
for desc in desc_results:
    print(desc.text)

for i in range(search_count):
    title = blog_results[i].text
    link = blog_results[i]['href']
    print(f'{title}, [{link}]')
    print(desc_results[i].text)
    print('-' * 80)