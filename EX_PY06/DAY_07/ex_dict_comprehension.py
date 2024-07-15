"""
List/Set/Dict 자료형과 반복문, 조건부표현식 결합
- 메모리 사용량 감소 & 속도 빠름
"""

keys = ["a", "b", "c", "d"]

x = {key : value for key, value in dict.fromkeys(keys).items()}

print(x)