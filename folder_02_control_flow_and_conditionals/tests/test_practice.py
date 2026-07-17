import pytest
from practice import is_even, grade_converter

def test_is_even():
    assert is_even(4) is True
    assert is_even(7) is False
    assert is_even(0) is True

def test_grade_converter():
    assert grade_converter(95) == 'A'
    assert grade_converter(82) == 'B'
    assert grade_converter(75) == 'C'
    assert grade_converter(60) == 'F'
