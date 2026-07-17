import pytest
from assignment import get_ticket_price

def test_get_ticket_price():
    assert get_ticket_price(70, False) == 10  # Senior
    assert get_ticket_price(70, True) == 10   # Senior Student (Senior discount > Student)
    assert get_ticket_price(20, True) == 12   # Adult Student
    assert get_ticket_price(10, True) == 8    # Child Student (Child discount > Student)
    assert get_ticket_price(30, False) == 15  # Regular Adult
    assert get_ticket_price(11, False) == 8   # Regular Child
