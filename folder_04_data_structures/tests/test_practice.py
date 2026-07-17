import pytest
from practice import get_last_element, add_key_value

def test_get_last_element():
    assert get_last_element([1, 2, 3]) == 3
    assert get_last_element(["a"]) == "a"
    assert get_last_element([]) is None

def test_add_key_value():
    assert add_key_value({"a": 1}, "b", 2) == {"a": 1, "b": 2}
    assert add_key_value({}, "x", 10) == {"x": 10}
