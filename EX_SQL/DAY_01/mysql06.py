import pymysql

conn = pymysql.connect(host = 'localhost', user = 'root', password = '1234',
                       db = 'sqlclass_db', charset = 'utf8')

curs = conn.cursor()

sql = """
    update customer
    set region = '서울특별시'
    where region = '서울'  
    """
curs.execute(sql)
print('update 완료')

sql = "delete from customer where name = %s"
curs.execute(sql, '홍길동')
print('delete 홍길동')

conn.commit()
curs.close()
conn.close()