import pytest
from assignment import get_word_frequencies

def test_get_word_frequencies():
    assert get_word_frequencies("The cat and the dog") == {"the": 2, "cat": 1, "and": 1, "dog": 1}
    assert get_word_frequencies("Hello hello Hello") == {"hello": 3}
    assert get_word_frequencies("") == {}
    assert get_word_frequencies("word WORD WoRd") == {"word": 3}
