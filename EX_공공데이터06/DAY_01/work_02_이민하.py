"""
- 윷가락은 4개의 값을 저장할 수 있도록 sticks=	[0,	0,	0,	0] 형태로 구현
- 윷을 던질 때 마다 랜덤하게 0,	1	사이의 값을 생성해서 sticks[]에 저장하고 점수를 계산함(예:	sticks[i]	=	random.randint(0,	1))
- 한 명의 점수가 먼저 20점 이상이면 게임은 바로 종료
- ‘모’나 ‘윷’이 나온 경우, 이미 총 점수가 20점 이상이면 한 번 더 던지지 않음
- 경기 시작은 어느 누구나 상관없음
- 게임이 종료되면 승패 결과를 화면에 출력하고 프로그램 종료
"""
import random

def check_total_score(total_score):
    if total_score >= 20:
        return 1
    else:
        return 0
    
def throw(sticks):
    for i in range(4):    
        sticks[i] = random.randint(0, 1)
    
    return sticks

def check_score(sticks):
    score = 0

    if sum(sticks) == 0:
        score += 5
    
    for i in range(4):
        score += sticks[i]     
    
    return score

def translate(sticks):
    if sum(sticks) == 0:
        print("모 (5점)", end = "")
    
    elif sum(sticks) == 1:
        print("도 (1점)", end = "")

    elif sum(sticks) == 2:
        print("개 (2점)", end = "")

    elif sum(sticks) == 3:
        print("걸 (3점)", end = "")

    elif sum(sticks) == 4:
        print("윷 (4점)", end = "")


def main():
    흥부 = 0
    놀부 = 0
    sticks = [0, 0, 0, 0]

    while True:
        score = 0
        throw(sticks)
        print(f"흥부 {sticks} : ", end = "")
        translate(sticks)
        score = check_score(sticks)
        if score >= 4:
            흥부 += score
            if check_total_score(흥부):
                print(f"/(총 {흥부}점) -->")
                print("-" * 20)
                print(f"흥부 승리 => 흥부 : {흥부}, 놀부 : {놀부}")
                print("-" * 20)
                break
            print(f"/(총 {흥부}점) -->")
            continue
        흥부 += score
        print(f"/(총 {흥부}점) -->")
        if check_total_score(흥부):
            print("-" * 20)
            print(f"흥부 승리 => 흥부 : {흥부}, 놀부 : {놀부}")
            print("-" * 20) 
            break

        score = 0
        throw(sticks)
        print(f"            <--- 놀부 {sticks} : ", end = "")
        translate(sticks)
        score = check_score(sticks)
        if score >= 4:
            놀부 += score
            if check_total_score(놀부):
                print(f"/(총 {놀부}점)")
                print("-" * 20)
                print(f"놀부 승리 => 흥부 : {흥부}, 놀부 : {놀부}")
                print("-" * 20)
                break
            print(f"/(총 {놀부}점)")
            continue
        놀부 += score
        print(f"/(총 {놀부}점)")
        if check_total_score(놀부):
            print("-" * 20)
            print(f"놀부 승리 => 흥부 : {흥부}, 놀부 : {놀부}")
            print("-" * 20)
            break

main()
        
        