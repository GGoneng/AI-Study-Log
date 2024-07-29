state = {"Seoul" : ["South Korea", "Asia", "9,655,000"],
         "Tokyo" : ["Japan", "Asia", "14,110,000"],
         "Beijing": ["China", "Asia", "21,540,000"],
         "London" : ["United Kingdom", "Europe", "14,800,000"],
         "Berlin" : ["Germany", "Europe", "3,426,000"],
         "Mexico City" : ["Mexico", "America", "21,200,000"]}

print(list(state.keys())[1])

for i in range(6):
    state.get(list(state.keys())[i])[2] = state.get(list(state.keys())[i])[2].replace(",", "")
    state.get(list(state.keys())[i])[2] = int(state.get(list(state.keys())[i])[2])

print(state)

while True:
    print("-" * 50)
    print(" 1. 전체 데이터 출력")
    print(" 2. 수도 이름 오름차순 출력")
    print(" 3. 모든 도시의 인구수 내림차순 출력")
    print(" 4. 특정 도시의 정보 출력")
    print(" 5. 대륙별 인구수 계산 및 출력")
    print(" 6. 프로그램 종료")
    print("-" * 50)

    
    state_list = list(state)
    values_list = list(state.values())

    opt = int(input("메뉴를 입력하세요 : "))

    if opt == 1:
        for i in range(len(state_list)):
            print(f"[{i + 1}] {state_list[i]} : {values_list[i]}")

    if opt == 2:
        capital_sorted_list = sorted(state.items(), key = lambda x : x[0])
        for i in range(len(capital_sorted_list)):
            print(f"[{i + 1}] {capital_sorted_list[i][0]:11s} : {capital_sorted_list[i][1][0]:15s}  {capital_sorted_list[i][1][1]:8s}  {capital_sorted_list[i][1][2]:,}")
        
    if opt == 3:
        population_sorted_list = sorted(state.items(), key = lambda x : x[1][2], reverse = True)
        for i in range(len(population_sorted_list)):
            print(f"[{i + 1}] {population_sorted_list[i][0]:11s} :  {population_sorted_list[i][1][2]:,}")

    if opt == 4:
        capital = input("출력할 도시 이름을 입력하세요 : ")
        result = state.get(capital, f"도시이름 : {capital}은 key에 없습니다.")
        if len(result) == 3:
            print(f"도시 : {capital}")
            print(f"국가 : {result[0]}, 대륙 : {result[1]}, 인구수 : {result[2]:,}")
        else:
            print(result)

    if opt == 5:
        population_sum = 0
        continent = input("대륙 이름을 입력하세요(Asia, Europe, America) : ")
        for i in range(len(state_list)):
            if continent == list(state.items())[i][1][1]:
                population_sum += values_list[i][2]
                print(f"{state_list[i]}: {values_list[i][2]:,}")
        print(f"{continent} 전체 인구수: {population_sum:,}")

    if opt == 6:
        print("프로그램을 종료합니다.")
        break