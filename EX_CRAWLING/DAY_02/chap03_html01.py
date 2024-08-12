from bs4 import BeautifulSoup

html_text = '<span class = "red">Heavens! what a virulent attack!</span>'
soup = BeautifulSoup(html_text, 'html.parser')

object_tag = soup.find('span')
print('object_tag : ', object_tag)
print('attrs : ', object_tag.attrs)
print('value : ', object_tag.attrs['class'])
print('text : ', object_tag.text)

