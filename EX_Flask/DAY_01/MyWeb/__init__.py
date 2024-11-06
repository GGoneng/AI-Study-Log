# -----------------------------------------------
# Flask Framework에서 WebServer 구동 파일
# - 파일명 : app.py
# -----------------------------------------------
# 모듈로딩 ---------------------------------------

from flask import Flask, render_template

# 사용자 정의 함수 -------------------------------
def create_app():
    # 전역변수 ----------------------------------
    # Flask Web Server 인스턴스 생성

    APP = Flask(__name__)

    # 라우팅 기능 모듈 ---------------------------
    from .views import main_views

    APP.register_blueprint(main_views.main_bp)

    return APP

# 조건부 실행 -----------------------------------
if __name__ == '__main__':
    # Flask Web Server 구동
    app = create_app()
    app.run()