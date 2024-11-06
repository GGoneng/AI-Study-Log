# -----------------------------------------------
# Flask Framework에서 '/'URL에 대한 라우팅 처리 파일
# - 파일명 : app.py
# -----------------------------------------------
# 모듈로딩 ---------------------------------------

from flask import Blueprint, render_template

# Blueprint 인스턴스 생성 ------------------------
main_bp = Blueprint('root', __name__, url_prefix = '/', template_folder = 'templates')

# 라우팅 기능 함수 정의 --------------------------
@main_bp.route('/', endpoint = 'hello')
def index():
    return render_template('index.html')