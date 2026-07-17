import pytest
from assignment import convert_celsius_to_fahrenheit

def test_convert_celsius_to_fahrenheit():
    assert convert_celsius_to_fahrenheit(0) == 32.0
    assert convert_celsius_to_fahrenheit(100) == 212.0
    assert convert_celsius_to_fahrenheit(-40) == -40.0
