from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen('https://en.wikipedia.org/wiki/Kevin_Bacon')
bs = BeautifulSoup(html, 'html.parser')
body_content = bs.find('div', {'id' : 'bodyContent'})

pattern = '^(/wiki/)((?!:).)*$'
for link in body_content.find_all('a', href = re.compile(pattern)):
    if 'href' in link.attrs:
        print(link.attrs['href'])