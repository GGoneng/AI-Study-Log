"""
Series / DataFrame에서 사용되는 사용자 정의 함수들
"""

# 함수 기능 : DataFrame의 기본정보와 속성 확인 기능
# 함수 이름 : checkDataFrame
# 매개 변수 : DataFrame 인스턴스 변수명, DataFrame 인스턴스 이름
# 리턴 값 / 반환 값 : None

def checkDataFrame(object, name):
    print(F"\n[{name}]")
    object.info()
    print(F"[Index] : {object.index}")
    print(F"[Columns] : {object.columns}")
    print(F"[Columns] : {object.ndim}")