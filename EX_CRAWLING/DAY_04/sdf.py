from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def get_kaggle_top_100(driver):
    driver.get('https://www.kaggle.com/rankings?group=datasets')
    time.sleep(5)  # 페이지 로드 대기

    # 스크롤 반복을 통해 데이터를 더 로드
    while len(driver.find_elements(By.CLASS_NAME, 'sc-bhjgvs')) < 100:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(3)  # 로드 대기

    # 이제 페이지에 로드된 이름 정보를 수집
    names_elements = driver.find_elements(By.CLASS_NAME, 'sc-bhjgvs')
    names = [elem.text for elem in names_elements[:100]]  # 상위 100개만 선택

    return names

def main():
    driver = webdriver.Chrome()
    try:
        names = get_kaggle_top_100(driver)
        for i, name in enumerate(names, 1):
            print(f"{i}: {name}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
