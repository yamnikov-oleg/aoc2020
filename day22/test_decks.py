import pytest

from decks import get_score, parse_decks


@pytest.mark.parametrize("content, decks", [
    (
        (
            "Player 1:\n"
            "9\n"
            "2\n"
            "6\n"
            "3\n"
            "1\n"
            "\n"
            "Player 2:\n"
            "5\n"
            "8\n"
            "4\n"
            "7\n"
            "10\n"
        ),
        ((9, 2, 6, 3, 1), (5, 8, 4, 7, 10)),
    ),
])
def test_parse_decks(content, decks):
    assert parse_decks(content) == decks


@pytest.mark.parametrize("deck, score", [
    ([3, 2, 10, 6, 8, 5, 9, 4, 7, 1], 306),
])
def test_get_score(deck, score):
    assert get_score(deck) == score
