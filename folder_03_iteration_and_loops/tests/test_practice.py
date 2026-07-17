import pytest
from practice import sum_to_n, find_first_negative

def test_sum_to_n():
    assert sum_to_n(5) == 15  # 1+2+3+4+5
    assert sum_to_n(1) == 1
    assert sum_to_n(10) == 55

def test_find_first_negative():
    assert find_first_negative([1, 2, -3, 4, -5]) == -3
    assert find_first_negative([1, 2, 3]) is None
    assert find_first_negative([-1, -2]) == -1
