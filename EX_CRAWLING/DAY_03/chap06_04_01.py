import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
from html_table_parser import parser_functions as parse
import pandas as pd

html = urlopen('http://en.wikipedia.org/wiki/Comparison_of_text_editors')
bs = BeautifulSoup(html, 'html.parser')

table = bs.find('table', {'class' : 'wikitable'})
table_data = parse.make2d(table)

print('[0] : ', table_data[0])
print('[1] : ', table_data[1])

df = pd.DataFrame(table_data[2:], columns = table_data[1])
print(df.head())

csvFile = open('editors1.csv', 'w', encoding = 'utf-8')
writer = csv.writer(csvFile)

for row in table_data:
    writer.writerow(row)

csvFile.close()