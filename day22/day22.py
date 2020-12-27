import combat
import reccombat
from decks import get_score, parse_decks


def main():
    with open('./input.txt') as f:
        deck1, deck2 = parse_decks(f.read())

    final_deck1, final_deck2, rounds_to_win = combat.play_until_win(deck1, deck2)
    winning_deck, winning_deck_number = combat.get_winning_deck(final_deck1, final_deck2)
    winning_score = get_score(winning_deck)
    print(f"Combat: Player {winning_deck_number} wins after {rounds_to_win} rounds with a score of {winning_score}")

    game_outcome = reccombat.play_until_win(deck1, deck2)
    print(f"Rec. combat: Player {game_outcome.winning_deck_number} wins with a score of {get_score(game_outcome.winning_deck)}")


if __name__ == "__main__":
    main()
