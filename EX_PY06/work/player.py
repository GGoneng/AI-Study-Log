class Player:
   
    def __init__(self, name):
        self.name = name
        self.holding_card_list = list()
        self.open_card_list = list()
    
    def add_card_list(self, card_list):
        for i in range(len(card_list)):
            self.holding_card_list.append(card_list[i])

    def display_two_card_lists(self):
        print(f"[{self.name}] Open card list : {len(self.open_card_list)}")
        
        for i in range(len(self.open_card_list)):
            print(self.open_card_list[i], end = " ")
            if (i + 1) % 13 == 0:
                print()
        print()
        print()

        print(f"[{self.name}] Holding card list : {len(self.holding_card_list)}")
        for i in range(len(self.holding_card_list)):
            print(self.holding_card_list[i], end = " ")
            if (i + 1) % 13 == 0:
                print()
        print()
        print()

    def check_one_pair_card(self):
        for i in range(len(self.holding_card_list) - 1):
            for j in range(i + 1, len(self.holding_card_list)):
                if (self.holding_card_list[i].number == self.holding_card_list[j].number) & (self.holding_card_list[i] not in self.open_card_list):
                    self.open_card_list.append(self.holding_card_list[i])
                    self.open_card_list.append(self.holding_card_list[j])

            for j in range(len(self.open_card_list)):
                if self.open_card_list[j] in self.holding_card_list:
                    self.holding_card_list.remove(self.open_card_list[j])
                    