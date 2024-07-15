"""
함수(Function) 이해 및 활용
함수 기반 계산기 프로그램
- 4칙 연산 기능별 함수 생성 => 덧셈, 뺄셈, 곱셈, 나눗셈
- 2개 정수만 계산
"""

def add(num1, num2):
    return num1 + num2

def sub(num1, num2):
    return num1 - num2

def mul(num1, num2):
    return num1 * num2

def div(num1, num2):
    if num2 == 0:
        return "잘못된 값입니다."
    else:    
        return num1 / num2

# - 사용자에게 원하는 계산을 선택하는 메뉴 출력
# - 종료 메뉴 선택 시 프로그램 종료
# => 반복 ---> 무한반복 : while

"""
함수 기능 : 계산기 메뉴를 출력하는 함수
함수 이름 : print_menu
매개 변수 : 
함수 결과 :
"""

# print(F"{'*':^16}") # 가운데 정렬
# print(F"{'*':>16}") # 오른쪽 정렬
# print(F"{'*':<16}") # 왼쪽 정렬

def print_menu():
    print(f"{'*':*^16}")
    print(f"* {'계 산 기':^9} *")
    print(f"{'*':*^16}")
    print(F"* {'1. 덧 셈':^10} *")
    print(F"* {'2. 뺄 셈':^10} *")
    print(F"* {'3. 곱 셈':^10} *")
    print(F"* {'4. 나 눗 셈':^9} *")
    print(F"* {'5. 종 료':^10} *")

"""
함수 기능 : 입력 받은 데이터가 유효한 데이터인지 검사하는 함수
함수 이름 : check_data
매개 변수 : str 데이터, 데이터 수
함수 결과 : boolean
"""

def check_data(data, length):
    check_decimal = True
    
    if len(data.split()) != length:
        print("개수가 맞지 않습니다.")
        return False
    
    else:
        for d in data.split():
            if not d.isdecimal():
                check_decimal = False
                break
        if check_decimal == True:
            print("올바른 데이터 입니다.")
            return True
        else:
            print("정수가 아닙니다.")
            return False

def calc(func, op):
    data = input("정수 2개(예 : 10 2) : ")
    if check_data(data, 2):
        data = data.split()
        print(F"결과 : {data[0]}{op}{data[1]} = {func(int(data[0]), int(data[1]))}")
    else:
        print(f"{data} : 올바른 데이터가 아닙니다.")

while True:    
    # 메뉴 출력
    print_menu()

    # 메뉴 선택 요청
    # choice = int(input("메뉴 선택 : "))
    choice = input("메뉴 선택 : ")
    if choice.isdecimal():
        choice = int (choice)
    else:
        print("0 ~ 9사이 숫자만 입력하세요.")
        continue

    # 종료 조건(5번 메뉴 선택) 처리
    if choice == 5:
        print("프로그램을 종료합니다.")
        break
    
    elif choice == 1: 
        print("덧셈")
        calc(add, "+")

    elif choice == 2: 
        print("뺄셈")
        data = input("정수 2개(예 : 10 2) : ")
        if check_data(data, 2):
            num1, num2 = data.split() 
            num1 = int(num1)
            num2 = int(num2)
            print(F"==> 결과 : {num1} + {num2} = {sub(num1, num2)}")
        else:
            continue
    
    elif choice == 3: 
        print("곱셈")
        data = input("정수 2개(예 : 10 2) : ")
        if check_data(data, 2):
            num1, num2 = data.split() 
            num1 = int(num1)
            num2 = int(num2)
            print(F"==> 결과 : {num1} + {num2} = {mul(num1, num2)}")
        else:
            continue

    elif choice == 4: 
        print("나눗셈")
        data = input("정수 2개(예 : 10 2) : ")
        if check_data(data, 2):
            num1, num2 = data.split() 
            num1 = int(num1)
            num2 = int(num2)
            print(F"==> 결과 : {num1} + {num2} = {div(num1, num2)}")
        else:
            continue

    else:
        print("선택된 메뉴는 없습니다.")
        
