import pytest
def test_len_phrase():
    phrase = input("Set a phrase: ")
    assert len(phrase) < 15, f"{phrase} больше 14 символов"
    print(phrase)