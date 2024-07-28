import csv

def get_minmax_temp(data):
    """
    최고 기온 및 최저 기온의 날짜 구하기
    """
    header = next(data)
    
    min_temp = 100
    min_date = ''

    max_temp = -999
    max_date = ''

    for row in data:
        if row[3] == '':
            row[3] = 100
        row[3] = float(row[3])

        if row[4] == '':
            row[4] = -999
        row[4] = float(row[4])

        if row[3] < min_temp:
            min_temp = row[3]
            min_date = row[0]
            print(F"최저기온 업데이트 : {min_date}, {min_temp}")

        if row[4] > max_temp:
            max_temp = row[4]
            max_date = row[0]
            print(F"최고기온 업데이트 : {max_date} {max_temp}")
        
    print('-' * 50)
    print(header)
    print(f"대구 최저 기온 날짜 : {min_date}, 온도 : {min_temp}")
    print(f"대구 최고 기온 날짜 : {max_date}, 온도 : {max_temp}")

def main():
    f = open("daegu-utf8.csv", encoding = "utf-8-sig")
    data = csv.reader(f)
    get_minmax_temp(data)
    f.close()

main()