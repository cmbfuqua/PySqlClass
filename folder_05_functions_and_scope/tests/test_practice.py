import pytest
import practice

def test_multiply():
    assert practice.multiply(3, 4) == 12
    assert practice.multiply(-2, 5) == -10
    assert practice.multiply(0, 100) == 0

def test_get_discounted_price():
    assert practice.get_discounted_price(100) == 90
    assert practice.get_discounted_price(100, 0.2) == 80
    assert practice.get_discounted_price(50, 0.5) == 25

def test_increment_counter():
    practice.COUNTER = 0
    practice.increment_counter()
    assert practice.COUNTER == 1
    practice.increment_counter()
    assert practice.COUNTER == 2
