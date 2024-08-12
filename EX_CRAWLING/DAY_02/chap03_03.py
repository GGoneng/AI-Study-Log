from urllib.request import urlopen
from bs4 import BeautifulSoup
import random
import re


random.seed(None)

def getLinks(articleUrl):
    html = urlopen('https://en.wikipedia.org' + articleUrl)
    bs = BeautifulSoup(html, 'html.parser')
    bodyContent = bs.find('div', {'id' : 'bodyContent'})
    wikiUrl = bodyContent.find_all('a', href = re.compile('^(/wiki/)((?!:).)*$'))
    return wikiUrl

links = getLinks('/wiki/Kevin_Bacon')
print('links 길이 : ', len(links))
while len(links) > 0:
    newArticle = links[random.randint(0, len(links) - 1)].attrs['href']
    print(newArticle)
    links = getLinks(newArticle)