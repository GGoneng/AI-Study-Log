
def printLPrices(L_p): # 함수 생성 (각 길이별 가격 출력)
    print("length :", end = '')
    for i in range(len(L_p)):
        print("{:3d}".format(i + 1), end = ', ') # 길이는 index + 1의 값을 써서 1 ~ 8까지 출력
    print("\nprice :", end = '')
    for i in range(len(L_p)):
        print("{:3d}".format(L_p[i]), end = ', ') # 가격은 가격 리스트에 index 값을 사용하여 출력
    print()

def printLCuttings(L_p, L_cuttings): # 함수 생성 (가장 이득을 보는 길이와 가격 출력)
    print('selected cuttings : ' , end = '')
    for i in range(len(L_cuttings)): # L_cuttings의 요소 개수 만큼 반복 출력
        print(('[length({}) : price({})]').format(L_cuttings[i], L_p[L_cuttings[i] - 1]), end = '')
    print('\n')

def cutRod(price, max_len): # 함수 생성 (막대기 자르기)
    val = [0 for x in range(max_len + 1)] # 막대기 길이별 가장 높은 가격을 적을 리스트 생성
    cuttings = [[None] for i in range(max_len + 1)] # 막대기 길이별 어느 길이로 잘라야 가장 이득인지 적을 리스트 생성

    for i in range(1, max_len + 1):
        max_val = 0 # 가장 높은 가격을 적을 변수 초기화
        for j in range(i):
            if max_val < price[j] + val[i - j - 1]: # max_val 보다 이전에 구해놓은 val[i - j - 1] + price[j] 값 보다 클 경우 (i와 j가 반복되며, 최댓값을 구함)
                max_val = price[j] + val[i - j - 1] # max_val을 비교하며 가장 큰 값으로 지정
                cuttings[i] = [j + 1] # 가장 큰 값을 얻은 쪼개기 길이를 cuttings에 저장
        val[i] = max_val # 가장 높은 가격은 val에 저장
    
    while True: # 무한 루프 생성
        if max_len - sum(cuttings[max_len]) > 0: # max_len 보다 cuttings의 마지막 리스트의 총합이 작을 경우 (최댓값을 얻는 쪼개진 막대 길이를 모두 구하기 위함)
            cuttings[max_len].append(cuttings[max_len - sum(cuttings[max_len])][0]) # cuttings[max_len] 위치에 추가
        
        else: # max_len이 cuttings[max_len]의 합보다 작을 경우 끝
            break

    return val[max_len], cuttings[max_len]


if __name__ == "__main__":
    L_pr_a = [1, 5, 8, 9, 10, 17, 18, 20]
    L_pr_b = [2, 5, 8, 11, 14, 17, 20, 23]
    L_pr_c = [3, 5, 8, 11, 14, 17, 20, 23]
    for L_name, L_p in [("case A", L_pr_a), ("case_B", L_pr_b), ("case_C", L_pr_c)]:
        print(L_name)
        printLPrices(L_p)
        max_len = len(L_p)
        max_rev, L_cuttings = cutRod(L_p, max_len)
        print("Maximum Obtainable Value with max length ({}) = {}".format(max_len, max_rev))
        printLCuttings(L_p, L_cuttings)
