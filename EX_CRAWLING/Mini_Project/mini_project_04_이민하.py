from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests


url = 'https://www.jobplanet.co.kr/companies/50695/salaries/(%EC%A3%BC)%ED%8B%B0%EB%AA%AC' 
html = requests.get(url)

soup = BeautifulSoup(html.text, 'html.parser')

job = soup.find_all("input")


# job = soup.find_all("div", {'class' : 'jply_ip_wrap'})


print(job)
