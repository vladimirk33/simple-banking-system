import random
from functools import reduce

CARDS = {}


def menu():
    print("""\n1. Create an account
2. Log into account
0. Exit""")


def take_response():
    response = input("> ")
    if response in ("0", "1", "2"):
        return response
    print("Choose correct menu item.")


def luhn(code):
    LOOKUP = (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)
    code = reduce(str.__add__, filter(str.isdigit, code))
    evens = sum(int(i) for i in code[-1::-2])
    odds = sum(LOOKUP[int(i)] for i in code[-2::-2])
    return (evens + odds) % 10 == 0


def create_card():
    BIN = "400000"
    checksum = "2"
    AI = str(random.randint(100000000, 999999999))
    card_number = BIN + AI + checksum
    while not luhn(card_number):
        AI = str(random.randint(100000000, 999999999))
        card_number = BIN + AI + checksum
    card_pin = str(random.randint(1000, 9999))
    CARDS[card_number] = card_pin
    return card_number, card_pin


def create_account():
    print()
    print("Your card has been created")
    card_number, card_pin = create_card()
    print("Your card number:\n" + card_number)
    print("Your card PIN\n" + card_pin)


def account_menu():
    print("""\n1. Balance
2. Log out
0. Exit""")


def print_balance():
    print("\nBalance: 0")


def login_account():
    print()
    card_number = input("Enter your card number:\n> ")
    card_pin = input("Enter your PIN:\n> ")
    try:
        if CARDS[card_number] == card_pin:
            print("\nYou have successfully logged in!")
            response = None
            while response != "2":
                account_menu()
                response = take_response()
                if response == "1":
                    print_balance()
                elif response == "0":
                    print("\nBye!")
                    exit(1)
                elif response == "2":
                    print("You have successfully logged out!")
        else:
            print("\nWrong card number or PIN!")
    except KeyError:
        print("\nWrong card number or PIN!")


def main():
    response = None
    while response != "0":
        menu()
        response = take_response()
        if response == "1":
            create_account()
        elif response == "2":
            login_account()
    print("\nBye!")


if __name__ == "__main__":
    main()
