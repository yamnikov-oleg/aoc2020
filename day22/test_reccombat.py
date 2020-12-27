from reccombat import play_until_win


def test_play_until_win():
    deck1 = (9, 2, 6, 3, 1)
    deck2 = (5, 8, 4, 7, 10)
    game_outcome = play_until_win(deck1, deck2)
    assert game_outcome.winning_deck == (7, 5, 6, 2, 4, 1, 10, 8, 9, 3)
