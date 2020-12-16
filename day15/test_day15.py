import pytest

from day15 import play_numbers_game


@pytest.mark.parametrize("starting_numbers,end_at,result", [
    ([1, 3, 2], 2020, 1),
    ([2, 1, 3], 2020, 10),
    ([1, 2, 3], 2020, 27),
    ([2, 3, 1], 2020, 78),
    ([3, 2, 1], 2020, 438),
    ([3, 1, 2], 2020, 1836),
    # ([0, 3, 6], 30000000, 175594),
    # ([1, 3, 2], 30000000, 2578),
    # ([2, 1, 3], 30000000, 3544142),
    # ([1, 2, 3], 30000000, 261214),
    # ([2, 3, 1], 30000000, 6895259),
    # ([3, 2, 1], 30000000, 18),
    # ([3, 1, 2], 30000000, 362),
])
def test_play_numbers_game(starting_numbers, end_at, result):
    assert play_numbers_game(starting_numbers, end_at) == result
