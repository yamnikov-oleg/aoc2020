from dataclasses import dataclass
from typing import Set, Tuple

from decks import Deck


@dataclass(frozen=True)
class GameOutcome:
    """
    Result of a game of Recursive Combat.

    :ivar winning_deck_number: 1 if the first player won, 2 if the second player won.
    :ivar final_deck1: The first deck after the end of the game.
    :ivar final_deck2: The second deck after the end of the game.
    """
    winning_deck_number: int  # 1 or 2
    final_deck1: Deck
    final_deck2: Deck

    @property
    def winning_deck(self) -> Deck:
        if self.winning_deck_number == 1:
            return self.final_deck1
        elif self.winning_deck_number == 2:
            return self.final_deck2
        else:
            raise ValueError(f"Invalid winning_deck_number: {self.winning_deck_number}")


@dataclass(frozen=True)
class Round:
    """
    Result of a single round of Recursive Combat (which may have included a sub game).

    :ivar winning_deck_number: 1 if the first player won, 2 if the second player won.
    :ivar final_deck1: The first deck after the end of the game.
    :ivar final_deck2: The second deck after the end of the game.
    :ivar game_over: True if the game has ended. The winner of this round is the winner of the game.
    """
    winning_deck_number: int  # 1 or 2
    final_deck1: Deck
    final_deck2: Deck
    game_over: bool = False


def play_a_round(deck1: Deck, deck2: Deck, played_decks: Set[Tuple[Deck, Deck]]) -> Round:
    """
    Plays a single round of Recursive Combat including the subgame if it occurs.

    :param played_decks: A set of pairs of decks played in this game previously.
    """
    if (deck1, deck2) in played_decks:
        return Round(
            winning_deck_number=1,
            final_deck1=deck1,
            final_deck2=deck2,
            game_over=True,
        )

    card1, subdeck1 = deck1[0], deck1[1:]
    card2, subdeck2 = deck2[0], deck2[1:]
    if len(subdeck1) >= card1 and len(subdeck2) >= card2:
        subgame_outcome = play_until_win(subdeck1[:card1], subdeck2[:card2])
        if subgame_outcome.winning_deck_number == 1:
            return Round(
                winning_deck_number=1,
                final_deck1=subdeck1 + (card1, card2),
                final_deck2=subdeck2,
            )
        elif subgame_outcome.winning_deck_number == 2:
            return Round(
                winning_deck_number=2,
                final_deck1=subdeck1,
                final_deck2=subdeck2 + (card2, card1),
            )
        else:
            raise ValueError(f"Invalid subgame outcome: {subgame_outcome!r}")

    if card1 > card2:
        return Round(
            winning_deck_number=1,
            final_deck1=subdeck1 + (card1, card2),
            final_deck2=subdeck2,
            game_over=len(subdeck2) == 0,
        )
    elif card2 > card1:
        return Round(
            winning_deck_number=2,
            final_deck1=subdeck1,
            final_deck2=subdeck2 + (card2, card1),
            game_over=len(subdeck1) == 0,
        )
    else:
        raise ValueError(f"Cards are equal: {deck1, deck2}")


def play_until_win(deck1: Deck, deck2: Deck) -> GameOutcome:
    """
    Plays full game of Recursive Combat.
    """
    played_decks = set()
    last_round: Round = None
    while True:
        last_round = play_a_round(deck1, deck2, played_decks)
        played_decks.add((deck1, deck2))
        deck1, deck2 = last_round.final_deck1, last_round.final_deck2

        if last_round.game_over:
            break

    return GameOutcome(
        winning_deck_number=last_round.winning_deck_number,
        final_deck1=deck1,
        final_deck2=deck2,
    )
