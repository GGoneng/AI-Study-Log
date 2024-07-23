"""
시각화 관련 함수들 존재하는 모듈
"""

"""
- 함수 기능 : 버전 체크 후 출력
- 함수 이름 : check_version 
- 매개 변수 : None
- 함수 결과 : None
"""

def chec

k_version():
    import matplotlib
    print(f"matplotlib : v{matplotlib.__version__}")
