import pytest
import assignment

def test_calculate():
    assert assignment.calculate(5, 3, 'add') == 8
    assert assignment.calculate(5, 3, 'subtract') == 2
    assert assignment.calculate(5, 3, 'multiply') == 15
    assert assignment.calculate(6, 3, 'divide') == 2
    assert assignment.calculate(5, 0, 'divide') is None
    assert assignment.calculate(5, 3, 'unknown') is None

def test_is_palindrome():
    assert assignment.is_palindrome("racecar") is True
    assert assignment.is_palindrome("hello") is False
    assert assignment.is_palindrome("A man a plan a canal Panama") is True
    assert assignment.is_palindrome("No lemon no melon") is True
    assert assignment.is_palindrome("Not a palindrome") is False
