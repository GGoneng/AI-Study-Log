from urllib.request import urlopen
from bs4 import BeautifulSoup
import random
import pymysql
import re

def store(conn, cur, title, content):
    cur.execute('INSERT INTO pages (title, content) VALUES ("%s", "%s")', (title, content))
    conn.commit()

def get_links(conn, cur, articleUrl):
    html = urlopen('http://en.wikipedia.org' + articleUrl)
    bs = BeautifulSoup(html, 'html.parser')

    title = bs.find('h1').text
    content = bs.find('div', {'id' : 'mw-content-text'}).find('p').text
    print(title, content)

    store(conn, cur, title, content)

    return bs.find('div', {'id' : 'bodyContent'}).find_all('a', href = re.compile('^(/wiki/)((?!:).)*$'))

def main():
    conn = pymysql.connect(host = 'localhost', user = 'root', passwd = '1234', db = 'scraping', charset = 'utf8')

    cur = conn.cursor()
    random.seed(None)

    links = get_links(conn, cur, '/wiki/Kevin_Bacon')
    try:
        while len(links) > 0:
            newArticle = links[random.randint(0, len(links) - 1)].attrs['href']
            print(newArticle)
            links = get_links(conn, cur, newArticle)

    finally:
        cur.close()
        conn.close()

main()