from typing import Tuple

from decks import Deck


def has_game_ended(deck1: Deck, deck2: Deck) -> bool:
    """
    Given two decks returns True if the game for these decks is over.
    """
    return len(deck1) == 0 or len(deck2) == 0


def play_a_round(deck1: Deck, deck2: Deck) -> Tuple[Deck, Deck]:
    """
    Plays one round of Combat and returns updated player decks.
    """
    if has_game_ended(deck1, deck2):
        return deck1, deck2

    if deck1[0] > deck2[0]:
        played_cards = (deck1[0], deck2[0])
        return deck1[1:] + played_cards, deck2[1:]
    elif deck2[0] > deck1[0]:
        played_cards = (deck2[0], deck1[0])
        return deck1[1:], deck2[1:] + played_cards
    else:
        raise ValueError(f"Deck's top cards are equal: {deck1}, {deck2}")


def play_until_win(deck1: Deck, deck2: Deck) -> Tuple[Deck, Deck, int]:
    """
    Plays full game of Combat and returns the final player decks and
    the total number of rounds played.
    """
    rounds = 0
    while not has_game_ended(deck1, deck2):
        deck1, deck2 = play_a_round(deck1, deck2)
        rounds += 1

    return deck1, deck2, rounds


def get_winning_deck(deck1: Deck, deck2: Deck) -> Tuple[Deck, int]:
    """
    Given two decks after the end of the game of Combat returns the deck
    of the winner and it's number (1 or 2).
    """
    if not deck1 and deck2:
        return deck2, 2
    elif not deck2 and deck1:
        return deck1, 1
    else:
        raise ValueError("The game has not ended")
