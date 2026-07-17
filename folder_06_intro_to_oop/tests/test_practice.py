import pytest
import practice

def test_car():
    my_car = practice.Car("Toyota", "Corolla")
    assert my_car.make == "Toyota"
    assert my_car.model == "Corolla"
    assert my_car.get_description() == "Make: Toyota, Model: Corolla"

def test_bank_account():
    account = practice.BankAccount()
    assert account.get_balance() == 0
    account.deposit(50)
    assert account.get_balance() == 50
    account.deposit(100)
    assert account.get_balance() == 150
