import pytest

from combat import play_until_win


@pytest.mark.parametrize("start_decks, final_decks, rounds", [
    (
        ((9, 2, 6, 3, 1), (5, 8, 4, 7, 10)),
        ((), (3, 2, 10, 6, 8, 5, 9, 4, 7, 1)),
        29,
    ),
])
def test_play_until_win(start_decks, final_decks, rounds):
    actual_final_deck1, actual_final_deck2, actual_rounds = play_until_win(*start_decks)
    assert (actual_final_deck1, actual_final_deck2) == final_decks
    assert actual_rounds == rounds
