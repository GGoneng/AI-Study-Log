from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('https://www.daangn.com/hot_articles')
print(type(html))
print()
print(html.read())