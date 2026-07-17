import pytest
from practice import greeting, calculate_area

def test_greeting():
    assert greeting() == "Hello, World!"

def test_calculate_area():
    assert calculate_area() == 50
