from typing import List, Tuple

Deck = List[int]


def parse_decks(content: str) -> Tuple[Deck, Deck]:
    deck_contents = content.strip().split('\n\n')
    decks = []
    for deck_content in deck_contents:
        cards = [int(line) for line in deck_content.split('\n')[1:]]
        decks.append(tuple(cards))

    if len(decks) != 2:
        raise ValueError(f"Content contains invalid number of decks: {len(decks)}")

    return decks[0], decks[1]


def get_score(deck: Deck) -> int:
    score = 0
    for card_index, card in enumerate(reversed(deck)):
        score += card * (card_index + 1)
    return score
