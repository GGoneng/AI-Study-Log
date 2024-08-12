from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen('http://www.pythonscraping.com/pages/page3.html')
soup = BeautifulSoup(html, 'html.parser')

# 정규식 : ('img.*.jpg): img 다음에 임의의 한 문자가 0회 이상
# -
img_tag = re.compile('/img/gifts/img.*.jpg')
images = soup.find_all('img', {'src' : img_tag})

for image in images:
    print(image, end = " -> ['src'] 속성값 : ")
    print(image['src'])