'''
저장된 hollys_branches.csv 파일을 읽어서 사용자가 입력한 지역에 존재하는 매장 검색 기능 구현
 - DataFrame으로 변경 후 DataFrame에서 값 검색 하기
'''

import pandas as pd
from tabulate import tabulate
import collections

collections.Callable = collections.abc.Callable

def print_branches(city_location_df):
    '''

    :param city_location_df: 입력된 지역에 위치한 매장의 DataFrame
    :return:
    '''
    #
    # DataFrame을 list로 변경: values.tolist()
    #
    # city_location_df = city_location_df.reset_index(drop=True)
    # city_location_df = city_location_df.set_axis(range(1, len(city_location_df)+1))
    city_location_df = (city_location_df
                        .reset_index(drop=True)
                        .set_axis(range(1, len(city_location_df)+1)))
    print(tabulate(city_location_df, headers='keys', tablefmt='psql'))
    print()


def main():
    df = pd.read_csv('hollys_branches.csv', encoding='utf-8')

    while True:
        # 검색할 지역 입력 ('quit' 입력시 프로그램 종료)
        city = input('검색할 매장의 지역을 입력하세요: ')

        if city == 'quit':
            print('종료 합니다.')
            break
        else:
            # str.contains(문자열):  문자열을 포함하고 있는 컬럼 검색
            city_df = df[df['지역'].str.contains(city)]
            city_location_df = pd.DataFrame(city_df, columns=('매장이름', '주소', '전화번호'))
            branch_count = city_location_df['매장이름'].count()

            if branch_count == 0:
                print('검색된 매장이 없습니다.')
            else:
                print('검색된 매장 수: ', branch_count)
                print_branches(city_location_df)


main()
