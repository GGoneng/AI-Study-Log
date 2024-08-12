from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com/pages/page3.html')
soup = BeautifulSoup(html, 'html.parser')

for sibling in soup.find('table', {'id' : 'giftList'}).tr.next_siblings:
    print(sibling)
    print('-' * 30)


print('previous_siblings')
for sibling in soup.find('tr', {'id' : 'gift2'}).previous_siblings:
    print(sibling)

sibling1 = soup.find('tr', {'id' : 'gift3'}).next_sibling
print('sibling1 : ', sibling1)
print(ord(sibling1))

sibling2 = soup.find('tr', {'id' : 'gift3'}).next_sibling.next_sibling
print(sibling2)

style_tag = soup.style
print(style_tag.parent)

img1 = soup.find('img', {'src' : '../img/gifts/img1.jpg'})
text = img1.parent.previous_sibling.get_text()
print(text)

