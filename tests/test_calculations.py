import pytest 
from app.calculations import * 

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(100)

@pytest.mark.parametrize('num1, num2, expected', [
    (3, 2, 5),
    (4, 4, 8),
    (12, 5, 17),
    (24, 56, 80)
])
def test_add(num1, num2, expected):
    # print('testing add function')
    assert add(num1, num2) == expected


def test_subtract():
    # print('testing add function')
    assert subtract(9, 4) == 5


def test_multiply():
    # print('testing add function')
    assert multiply(5, 3) == 15


def test_divide():
    # print('testing add function')
    assert divide(12, 6) == 2


#reference to fixtures:
def test_bank_account_default_balance(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_bank_account_initial_balance(bank_account):
    assert bank_account.balance == 100
   

def test_bank_account_withdraw(bank_account):
    bank_account.withdraw(20)
    assert  bank_account.balance == 80


def test_bank_account_deposit(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 120


def test_bank_account_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 4) == 110


@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (50, 30, 20),
    (4500, 350, 4150),
])
def test_bank_transactions(zero_bank_account,deposited, withdrew, expected) :
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected


def test_insufficent_balance(bank_account):
    with pytest.raises(InsufficientFunds): 
        bank_account.withdraw(200)

