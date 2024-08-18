from card import Card
import random

class GameDealer:
    
    def __init__(self):
        self.deck = list()
        self.suit_number = 13
    
    def make_deck(self):
        card_suits = ["♠", "♥", "♣", "◆"]
        card_numbers = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

        for i in range(len(card_suits)):
            for j in range(len(card_numbers)):
                self.deck.append(Card(card_suits[i], card_numbers[j]))

        return self.deck

    def print_deck(self):
        for i in range(len(self.deck)):
            print(self.deck[i], end = " ")
            if (i + 1) % self.suit_number == 0:
                print()
        print()

    def shuffle_deck(self):
        random.shuffle(self.deck)


if __name__ == "__main__":
    gamedealer = GameDealer()
    
    print("[GmaeDealer] 초기 카드 생성")
    print("-" * 60)

    deck = gamedealer.make_deck()
    
    print(f"[GameDealer] 딜러가 가진 카드 수 {len(deck)}")
    
    gamedealer.print_deck()

    print("[GameDealer] 카드 랜덤하게 섞기")
    print("-" * 60)
    print(f"[GameDealer] 딜러가 가진 카드 수 {len(deck)}")
    
    gamedealer.shuffle_deck()
    gamedealer.print_deck()