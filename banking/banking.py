import sqlite3
import random
from functools import reduce

conn = sqlite3.connect("card.s3db")
cur = conn.cursor()


def create_db():
    cur.execute("""CREATE TABLE IF NOT EXISTS card (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         number TEXT,
                         pin TEXT,
                         balance INTEGER DEFAULT 0
                        );""")
    # for row in cur.execute('SELECT * FROM card'):
    #    print(row)
    conn.commit()


def menu():
    print("""\n1. Create an account
2. Log into account
0. Exit""")


def take_response():
    response = input("> ")
    if response in ("0", "1", "2", "3", "4", "5"):
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
    card_numbers = cur.execute("SELECT number FROM card").fetchall()
    if card_number in (i[0] for i in card_numbers):
        create_card()
    card_pin = str(random.randint(1000, 9999))
    cur.execute("INSERT INTO card VALUES (?, ?, ?, ?)",
                (None, card_number, card_pin, 0))
    conn.commit()
    return card_number, card_pin


def create_account():
    print()
    print("Your card has been created")
    card_number, card_pin = create_card()
    print("Your card number:\n" + card_number)
    print("Your card PIN:\n" + card_pin)


def account_login(card_number, card_pin):
    cur.execute("SELECT pin FROM card WHERE number = ?", [card_number])
    try:
        pin = cur.fetchone()[0]
    except TypeError:
        return False
    if card_pin == pin:
        return True
    return False


def account_menu():
    print("""\n1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")


def get_account_balance(card_number):
    cur.execute("SELECT balance FROM card WHERE number = ?", [card_number])
    return cur.fetchone()[0]


def add_income(card_number):
    income = int(input("\nEnter income:\n> "))
    balance = get_account_balance(card_number)
    balance += income
    if income > 0:
        cur.execute("UPDATE card SET balance = ? WHERE number = ?;",
                    [balance, card_number])
        conn.commit()
        print("Income was added!")


def do_transfer(card_number):
    print("\nTransfer")
    other_card = input("Enter card number:\n> ")
    card_numbers = cur.execute("SELECT number FROM card").fetchall()
    if not luhn(other_card):
        print("Probably you made a mistake in the card number. Please try again!")
        return
    elif other_card not in (i[0] for i in card_numbers):
        print("Such a card does not exist.")
        return
    transfer_money = int(input("Enter how much money you want to transfer:\n> "))
    balance = get_account_balance(card_number)
    if transfer_money > balance:
        print("Not enough money!")
        return
    balance = balance - transfer_money
    cur.execute("UPDATE card SET balance = ? WHERE number = ?;",
                [balance, card_number])
    other_balance = get_account_balance(other_card) + transfer_money
    cur.execute("UPDATE card SET balance = ? WHERE number = ?;",
                [other_balance, other_card])
    conn.commit()
    print("Success!")


def close_account(card_number):
    cur.execute("DELETE FROM card WHERE number = ?", [card_number])
    conn.commit()
    print("The account has been closed!")


def login_account():
    print()
    card_number = input("Enter your card number:\n> ")
    card_pin = input("Enter your PIN:\n> ")
    try:
        if account_login(card_number, card_pin):
            print("\nYou have successfully logged in!")
            response = None
            while response != "5":
                account_menu()
                response = take_response()
                if response == "1":
                    balance = get_account_balance(card_number)
                    print("\nBalance: " + str(balance))
                elif response == "2":
                    add_income(card_number)
                elif response == "3":
                    do_transfer(card_number)
                elif response == "4":
                    close_account(card_number)
                    response = "5"
                elif response == "5":
                    print("You have successfully logged out!")
                elif response == "0":
                    print("\nBye!")
                    exit(1)
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
    create_db()
    main()
