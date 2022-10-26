from app.calculation import add, subtract, multiply, divide, BankAccount, InsufficentFunds
import pytest

from tests.conftest import SQLALCHEMY_DATABSE_URL


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [
    (3, 1, 4),
    (5, 7, 12),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    raise Exception(SQLALCHEMY_DATABSE_URL)
    print("testing add function")
    assert add(num1, num2) == expected


def test_sub():
    print("testing subtract function")
    assert subtract(9, 3) == 6


def test_mul():
    print("testing multiply function")
    assert multiply(5, 3) == 15


def test_div():
    print("testing divide function")
    assert divide(15, 3) == 5


def test_bank(bank_account):

    assert bank_account.balance == 50


def test_withdraw():
    bank_account = BankAccount(50)
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_deposit():
    bank_account = BankAccount(80)
    bank_account.deposit(20)
    assert bank_account.balance == 100


def test_intrest():
    bank_account = BankAccount(50)
    bank_account.intrest()
    assert round(bank_account.balance, 6) == 55


@pytest.mark.parametrize("deposited, withdrew, expected", [
    (300, 100, 200),
    (500, 200, 300),
    (400, 200, 200)
])
def test_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected


def test_insufficent(bank_account):
    with pytest.raises(InsufficentFunds):
        bank_account.withdraw(1000)
