"""
마방진 만들기
시작은 항상 맨위 중앙
n X n 구조
1) 다음 위치는 오른쪽 대각선 방향으로 이동 (y2=y1-1,	x2=x1+1)
2) y축 방향으로 범위가 벗어난 경우, y는 마지막 행(size-1)으로 이동
3) x축 방향으로 범위가 벗어난 경우, x는 첫 번째 열(0)으로 이동
4) 다음 이동 위치에 이미 값이 있는 경우, y는 y	+ 1
"""

def make_square(size):
    Magic_square = [[0 for col in range(size)] for row in range(size)]

    return Magic_square

def start(size, square):
    square[0][size // 2] = 1
    row = 0
    col = size // 2
    num = 1
    
    return square, row, col, num

def move(square, row, col, num, size):
    for i in range(size * size - 1):
        num += 1
        if (row - 1 == -1 and col + 1) >= size:
            square[row + 1][col] = num
            row += 1

        elif col + 1 >= size:
            square[row - 1][0] = num
            row -= 1
            col = 0

        elif row - 1 == -1:
            if square[size - 1][col + 1] > 0:
                square[row + 1][col] = num        
                row += 1
            else:
                square[row + size - 1][col + 1] = num
                row += size - 1
                col += 1
        

        
        elif square[row - 1][col + 1] > 0:
            square[row + 1][col] = num
            row += 1

        else:
            square[row - 1][col + 1] = num   
            row -= 1
            col += 1     
    return square

def main():
    while True:
        size = int(input("홀수차 배열의 크기를 입력하세요 : "))
        if size % 2 == 0:
            print("짝수를 입력하였습니다. 다시 입력하세요.")
            continue
        else:
            break
    
    magic_square = make_square(size)
    square, row, col, num = start(size, magic_square)
    magic_square = move(square, row, col, num, size)
    for i in range(size):
        for j in range(size):
            print("{:3d}".format(magic_square[i][j]), end = "")
        print()

main()