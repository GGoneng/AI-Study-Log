from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get('https://www.google.com/search?q=' + 'Python')

driver.implicitly_wait(3)

search_results = driver.find_elements(By.CSS_SELECTOR, 'div.yuRUbf')
print(len(search_results))

for result in search_results:
    title_element = result.find_element(By.CSS_SELECTOR, "h3")
    title = title_element.text.strip()
    print(f"{title}")

driver.quit()