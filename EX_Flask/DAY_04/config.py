import os

# SQLite3 RDBMS 파일 경로 관련
BASE_DIR = os.path.dirname(__file__)
DB_NAME = 'moviedb.db'

# DB관련 기능 구현 시 사용할 전역변수
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://minha:1234@172.20.81.160/{DB_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
