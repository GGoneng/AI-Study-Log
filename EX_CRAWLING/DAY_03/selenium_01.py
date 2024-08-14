from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get("https://www.selenium.dev/selenium/web/web-form.html")

print(driver.title)
print(driver.page_source)
time.sleep(2)
driver.quit()