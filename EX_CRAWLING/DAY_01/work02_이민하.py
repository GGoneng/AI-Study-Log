class VendingMachine:
    def __init__(self, input_dict):
        self.input_money = 0 
        self.inventory = input_dict

    def exit(self):
        print("-" * 50)
        print("커피 자판기 동작을 종료합니다.")
        print("-" * 50)

    def menu(self):
        print("-" * 40)
        print(f"  커피 자판기 (잔액 : {self.input_money}원)")
        print("-" * 40)

        print(" 1. 블랙 커피")
        print(" 2. 프림 커피")
        print(" 3. 설탕 프림 커피")
        print(" 4. 재료 현황")
        print(" 5. 종료")
    
    def print_inventory(self):
        print("-" * 100)
        print(f"재료 현황 : ", end = "")
        for item, num in self.inventory.items():
            print(f"{item} : {num}", end = "  ")
        print()
        print("-" * 100)

    def check_inventory(self):
        empty = False

        if (self.inventory['coffee'] <= 0) or (self.inventory['cream'] <= 0) or (self.inventory['sugar'] <= 0) or (self.inventory['water'] <= 0):
            empty = True
            print("재료가 부족합니다.")
            print(f"{self.input_money}원을 반환합니다.")
            self.exit()

        return empty
                
    def select_menu(self):
        option = int(input("메뉴를 선택하세요 : "))
        if option == 1:
            self.input_money -= 300
            print(f"블랙 커피를 선택하셨습니다. 잔액 : {self.input_money}")
            self.inventory['coffee'] -= 30
            self.inventory['water'] -= 100
            self.inventory['cup'] -= 1
            self.inventory['change'] += 300
            self.print_inventory()

        elif option == 2:
            self.input_money -= 300
            print(f"프림 커피를 선택하셨습니다. 잔액 : {self.input_money}")
            self.inventory['coffee'] -= 15
            self.inventory['cream'] -= 15
            self.inventory['water'] -= 100
            self.inventory['cup'] -= 1
            self.inventory['change'] += 300
            self.print_inventory()

        elif option == 3:
            self.input_money -= 300
            print(F"설탕 프림 커피를 선택하셨습니다. 잔액 : {self.input_money}")
            self.inventory['coffee'] -= 10
            self.inventory['cream'] -= 10
            self.inventory['sugar'] -= 10
            self.inventory['water'] -= 100
            self.inventory['cup'] -= 1
            self.inventory['change'] += 300
            self.print_inventory()

        elif option == 4:
            self.print_inventory()

        elif option == 5:
            print(f"종료를 선택했습니다. {self.input_money}원이 반환됩니다.")
            self.exit()
            return option


    def insert_coin(self):
        self.input_money = int(input("동전을 투입하세요 : "))

    def run(self):
        
        self.insert_coin()
        
        if self.input_money < 300:
            print(f"투입된 돈 ({self.input_money}원)이 300원보다 작습니다.")
            print(f"{self.input_money}원을 반환합니다.")
            self.exit()
        
        else:
            while True:
                self.menu()
                option = self.select_menu()
                if option == 5:
                    break

                if self.input_money < 300:
                    print(f"잔액이 ({self.input_money}원)이 300원보다 작습니다.")
                    print(f"{self.input_money}원을 반환합니다.")
                    self.exit()
                    break

                if self.check_inventory(): break



inventory_dict = {'coffee' : 100, 'cream' : 100, 'sugar' : 100,
                  'water' : 500, 'cup' : 5, 'change' : 0}
coffee_machine = VendingMachine(inventory_dict)
coffee_machine.run()
