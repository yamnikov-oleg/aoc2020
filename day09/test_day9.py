from day9 import find_first_invalid_number, find_contiguous_sum


def test_find_first_invalid_number():
    assert find_first_invalid_number(
        [
            35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150,
            182, 127, 219, 299, 277, 309, 576,
        ],
        lookbehind=5,
    ) == 127


def test_find_contiguous_sum():
    assert find_contiguous_sum(
        [
            35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150,
            182, 127, 219, 299, 277, 309, 576,
        ],
        target=127,
    ) == [15, 25, 47, 40]
