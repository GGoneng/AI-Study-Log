from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import requests
import collections

def make_url_list(driver):
   
    frame = driver.find_element(By.XPATH, '//*[@id="site-content"]/div[2]/div/div/div[4]/div/div/div[2]/div/div/div[1]/div[1]')
    actions = ActionChains(driver)   
    
    soup = []
    
    actions.click(frame).perform()

    for j in range(50):

        driver.implicitly_wait(3)
        try:
            for i in range(1, 11):
                soup.append(driver.find_element(By.XPATH, f'//*[@id="site-content"]/div[2]/div/div/div[4]/div/div/div[2]/div/div/div[{i}]/div[3]/div/div/a[2]').get_attribute('href'))
            actions.send_keys(Keys.PAGE_DOWN)
            actions.send_keys(Keys.PAGE_DOWN)
            actions.send_keys(Keys.PAGE_DOWN)
            actions.send_keys(Keys.PAGE_DOWN)
            actions.send_keys(Keys.PAGE_DOWN)
            actions.perform()
        except Exception as e:
            continue        
    return soup

   

def crawling_text(url, msg, driver):

    driver.get(url)
    driver.implicitly_wait(3)
    msg += driver.find_element(By.CSS_SELECTOR, 'div.sc-cjHuto.edyDPE').text
    
    return msg

def main():
    driver = webdriver.Chrome()
    url = f'https://www.kaggle.com/rankings?group=datasets'
    driver.get(url)
    
    url_list = make_url_list(driver)

    msg = ""

    for name in set(url_list):
        try:
            print(name)
            msg = crawling_text(name, msg, driver)

        except Exception as e:
            continue

    file_path = 'output.txt'

    with open(file_path, 'w', encoding = 'utf-8') as file:
        file.write(msg)

    print(len(set(url_list)))
main()
