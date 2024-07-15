age = int(input())
balance = 9000

if 7 <= age <= 12:
    balance -= 650

elif 13 <= age <= 18:
    balance -= 1050

elif age >= 19:
    balance -= 1250

print(balance)