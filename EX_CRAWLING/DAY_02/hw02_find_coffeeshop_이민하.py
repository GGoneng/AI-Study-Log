import pandas as pd
import re
from tabulate import tabulate

def load_csv(file_name):
    data = pd.read_csv(file_name)
    
    return data

def search_store(area, data):
    for i in range(len(area)):
        data = data[(data['주소'].apply(lambda x : area[i] in x)) & (data['주소'].apply(lambda x : x.find(area[i])) < 9)]
    
    return data

def print_store(data):
    print(f"검색된 매장 수 : {len(data)}")
    print(tabulate(data[['매장이름', '주소', '전화번호']], headers = 'keys', tablefmt = 'psql', showindex = [i + 1 for i in range(len(data))]))
    print()

def main():
    while True:
        area = list(input("검색할 매장의 지역을 입력하세요 : ").split())

        if 'quit' in area:
            print("종료 합니다.")
            break

        
        data = load_csv('hollys_branches.csv')
        data = search_store(area, data)
        if len(data) == 0:
            print("검색된 매장이 없습니다.\n")
        else:    
            print_store(data)
main()    
