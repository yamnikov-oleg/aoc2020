from typing import Dict, List, Optional, Tuple


def play_numbers_game(starting_numbers: List[int], end_at: int) -> int:
    turns_played = 0
    last_number = None
    # Maps each number to the last two turns when it was spoken.
    # Each turn number is 0-based.
    spoken_at_turns: Dict[int, Tuple[Optional[int], Optional[int]]] = {}

    def say(number: int) -> None:
        nonlocal last_number
        last_number = number

        _, last_turn = spoken_at_turns.get(number, (None, None))
        spoken_at_turns[number] = (last_turn, turns_played)

    for number in starting_numbers:
        say(number)
        turns_played += 1

    while turns_played < end_at:
        if (turns_played % 1_000_000) == 0:
            print(turns_played, "turns played")

        second_to_last_turn, last_turn = spoken_at_turns[last_number]
        if second_to_last_turn is None:
            say(0)
            turns_played += 1
            continue
        else:
            age = last_turn - second_to_last_turn
            say(age)
            turns_played += 1
            continue

    return last_number


def main():
    starting_numbers = [8, 13, 1, 0, 18, 9]

    number_2020 = play_numbers_game(starting_numbers, 2020)
    print(f"2020th number: {number_2020}")

    number_30000000 = play_numbers_game(starting_numbers, 30_000_000)
    print(f"30000000th number: {number_30000000}")


if __name__ == "__main__":
    main()
