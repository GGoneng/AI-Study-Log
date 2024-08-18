from card import Card
from player import Player
from gamedealer import GameDealer

def play_game():
    player1 = Player("흥부")
    player2 = Player("놀부")

    dealer = GameDealer()
    dealer.make_deck()
    dealer.shuffle_deck()
    
    num = 10
    player1.add_card_list(dealer.deck[:num])
    for i in range(num):
        dealer.deck.pop(0)
    
    player2.add_card_list(dealer.deck[:num])
    for i in range(num):
        dealer.deck.pop(0)

    print("=" * 60)
    print(f"카드 나누어 주기 : {num}장")
    print("-" * 60)
    
    print(f"[GameDealer] 딜러가 가진 카드 수 : {len(dealer.deck)}")

    dealer.print_deck()
    print("=" * 60)

    player1.display_two_card_lists()
    print("=" * 60)
    player2.display_two_card_lists()

    level = 2
    next = input(f"[{level}]단계: 다음 단계 진행을 위해 Enter 키를 누르세요!")
    if next == "":
        print("=" * 60)
        print(f"[{player1.name}: 숫자가 같은 한쌍의 카드 검사]")
        print("=" * 60)

        player1.check_one_pair_card()
        player1.display_two_card_lists()

        print("=" * 60)
        print(f"[{player2.name}: 숫자가 같은 한쌍의 카드 검사]")
        print("=" * 60)

        player2.check_one_pair_card()
        player2.display_two_card_lists()

        level += 1

    else:
        print("다시 입력해주세요.")


    while (len(dealer.deck) > 0) & (len(player1.holding_card_list) > 0) & (len(player2.holding_card_list) > 0):
        next = input(f"[{level}]단계 : 다음 단계 진행을 위해 Enter 키를 누르세요!")
        if next == "":
            num = 4
            player1.add_card_list(dealer.deck[:num])
            for i in range(num):
                dealer.deck.pop(0)
            
            player2.add_card_list(dealer.deck[:num])
            for i in range(num):
                dealer.deck.pop(0)

            print("=" * 60)
            print(f"카드 나누어 주기 : {num}장")
            print("-" * 60)

            print(f"[GameDealer] 딜러가 가진 카드 수 : {len(dealer.deck)}")


            dealer.print_deck()
            print("=" * 60)

            print(f"[{player1.name}: 숫자가 같은 한쌍의 카드 검사]")
            print("=" * 60)

            player1.check_one_pair_card()
            player1.display_two_card_lists()

            print("=" * 60)
            print(f"[{player2.name}: 숫자가 같은 한쌍의 카드 검사]")
            print("=" * 60)

            player2.check_one_pair_card()
            player2.display_two_card_lists()
            
            level += 1

if __name__ == '__main__':
    play_game()