def add(num1: int, num2: int):
    return num1 + num2


def subtract(num1: int, num2: int):
    return num1 - num2


def multiply(num1: int, num2: int):
    return num1 * num2


def divide(num1: int, num2: int):
    return num1 / num2


class InsufficentFunds(Exception):
    pass


class BankAccount():
    def __init__(self, starting_balance=0) -> None:
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficentFunds("Insufficent money")
        self.balance -= amount

    def intrest(self):
        self.balance *= 1.1
