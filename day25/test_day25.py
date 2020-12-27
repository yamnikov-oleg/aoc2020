from day25 import find_loop_size, make_encryption_key


def test_find_loop_size():
    assert find_loop_size(5764801) == 8
    assert find_loop_size(17807724) == 11


def test_make_encryption_key():
    assert make_encryption_key(17807724, 8) == 14897079
    assert make_encryption_key(5764801, 11) == 14897079
