from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class CupList:
    """
    Basically, a linked list of ints.
    """
    value: int
    next_cup: Optional['CupList']

    def get_last(self) -> 'CupList':
        """
        Gets the last item in the list.
        Will loop forever if the list is circular.
        """
        if self.next_cup is None:
            return self
        else:
            return self.next_cup.get_last()

    def remove_next(self) -> 'CupList':
        """
        Removes the item after this one from the list.
        Returns the removed item.
        """
        removed_cup = self.next_cup
        self.next_cup = removed_cup.next_cup
        removed_cup.next_cup = None
        return removed_cup

    def find(self, value: int) -> Optional['CupList']:
        """
        Finds the first item with the given value and returns it.
        Or returns None if the item was not found.

        Works as expected even if the list is looped.
        """
        current_cup = self
        while True:
            if current_cup.value == value:
                return current_cup
            elif not current_cup.next_cup or current_cup.next_cup == self:
                return None
            else:
                current_cup = current_cup.next_cup

    def insert_next(self, cups: 'CupList'):
        """
        Inserts another list into this list after this item.
        """
        cups.get_last().next_cup = self.next_cup
        self.next_cup = cups

    def to_list(self, before: Optional['CupList'] = None) -> List[int]:
        """
        Converts this linked list into a python list of values.
        """
        if not self.next_cup or self.next_cup == before:
            return [self.value]
        else:
            return [self.value, *self.next_cup.to_list(before=before or self)]


@dataclass
class CupCircle:
    """
    A wrapper around CupList providing methods to play the game of cups.

    :ivar cups: The underlying list of cups. Must be circular.
        Do not edit this list directly, because it might invalidate CupCircle's inner state.
    """
    cups: CupList = field()
    # Maps cup values to the cups for quick access
    _cup_index: Dict[int, CupList] = field(init=False, compare=False, repr=False)
    # The cup with a maximum value
    _max_cup: CupList = field(init=False, compare=False, repr=False)

    def __post_init__(self):
        # Fill in the _cup_index and _max_cup attributes.
        current_cup = self.cups
        self._cup_index = {}
        self._max_cup = self.cups

        while True:
            self._cup_index[current_cup.value] = current_cup

            if current_cup.value > self._max_cup.value:
                self._max_cup = current_cup

            current_cup = current_cup.next_cup
            if current_cup == self.cups:
                break

    def pick_up(self, n: int) -> CupList:
        """
        Removes next n cups from the circle and returns them as a linked list.
        It's expected that the cups will be immediately put back into the circle
        with the place_after method.
        """
        first_cup = self.cups.remove_next()

        if n > 1:
            first_cup.next_cup = self.pick_up(n - 1)

        return first_cup

    def place_after(self, value: int, picked_up: CupList) -> None:
        """
        Put a list of cups after the cup with the given value.
        """
        cup = self._cup_index[value]
        cup.insert_next(picked_up)

    def move_to_next(self):
        """
        Selects next cup as a current cup.
        """
        self.cups = self.cups.next_cup

    def get_max_cup(self) -> CupList:
        """
        Returns the cup with the maximum value.
        """
        return self._max_cup

    def play_round(self):
        """
        Plays one round of the game.
        Picks up 3 cups and places them into a different part of the circle.
        """
        picked_up = self.pick_up(3)
        picked_up_values = picked_up.to_list()

        dest = self.cups.value - 1
        while True:
            if dest in picked_up_values or dest not in self._cup_index:
                dest -= 1
                if dest < 1:
                    dest = self.get_max_cup().value
            else:
                self.place_after(dest, picked_up)
                break

        self.move_to_next()

    def get_part1_answer(self) -> str:
        one_cup = self._cup_index[1]
        values = one_cup.next_cup.to_list(before=one_cup)
        return ''.join(str(v) for v in values)

    def get_previous_cup(self) -> 'CupList':
        """
        Returns the cup before the current cup.
        """
        current_cup = self.cups
        while current_cup.next_cup != self.cups:
            current_cup = current_cup.next_cup
        return current_cup

    def expand_to(self, n: int):
        """
        Adds more cups before the current cup to make total cups number into n.
        """
        max_value = self.get_max_cup().value
        last_cup = self.get_previous_cup()
        for value in range(max_value + 1, n + 1):
            new_cup = CupList(value=value, next_cup=self.cups)
            last_cup.next_cup = new_cup
            self._cup_index[value] = new_cup
            self._max_cup = new_cup

            last_cup = new_cup

    def get_part2_answer(self) -> int:
        one_cup = self._cup_index[1]
        cup1 = one_cup.next_cup
        cup2 = cup1.next_cup
        return cup1.value * cup2.value


def parse_cup_circle(s: str) -> CupCircle:
    def _parse_cups(s: str) -> Optional[CupList]:
        if len(s) == 0:
            return None
        else:
            return CupList(value=int(s[0]), next_cup=_parse_cups(s[1:]))

    cups = _parse_cups(s)
    cups.get_last().next_cup = cups

    return CupCircle(cups=cups)


def main():
    INPUT = "398254716"

    circle = parse_cup_circle(INPUT)
    for i in range(100):
        circle.play_round()
    print(f"Answer after 100 rounds: {circle.get_part1_answer()}")

    circle = parse_cup_circle(INPUT)
    circle.expand_to(1_000_000)
    for i in range(10_000_000):
        if i % 1_000_000 == 0:
            print(f"{i} rounds played")
        circle.play_round()
    print(f"Answer after 10M rounds: {circle.get_part2_answer()}")


if __name__ == "__main__":
    main()
