from urllib.request import urlopen
from bs4 import BeautifulSoup

melon_url = 'https://www.melon.com/chart/index.htm'
html = urlopen(melon_url)

soup = BeautifulSoup(html.read(), 'html.parser')
print(soup)