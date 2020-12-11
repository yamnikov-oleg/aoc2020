from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, Iterator, List, Optional, Tuple


class CellState(Enum):
    FLOOR = auto()
    SEAT_EMPTY = auto()
    SEAT_OCCUPIED = auto()


@dataclass
class Area:
    # (row, column): state
    # Top-most row is row 0
    # Left-most column is column 0
    _cell_map: Dict[Tuple[int, int], CellState] = field(default_factory=dict)
    _max_row_index: int = 0
    _max_column_index: int = 0

    def get(self, row: int, column: int) -> Optional[CellState]:
        return self._cell_map.get((row, column))

    def set(self, row: int, column: int, state: CellState):
        self._cell_map[(row, column)] = state

        if row > self._max_row_index:
            self._max_row_index = row

        if column > self._max_column_index:
            self._max_column_index = column

    def get_max_row_index(self) -> int:
        return self._max_row_index

    def get_max_column_index(self) -> int:
        return self._max_column_index

    def clone(self) -> 'Area':
        return Area(_cell_map=self._cell_map.copy())

    def __iter__(self) -> Iterator[Tuple[int, int, CellState]]:
        """
        Iterates over the area row by row starting from the top (row 0)
        then column by column starting from the left (column 0).

        Yields row index, column index and the cell's state in a tuple
        on each iteration.
        """
        for row_index in range(self.get_max_row_index() + 1):
            for column_index in range(self.get_max_column_index() + 1):
                state = self.get(row_index, column_index)
                if state is None:
                    continue

                yield row_index, column_index, state

    def step(self) -> 'Area':
        """
        Advances the waiting area state by one step.
        Returns the updated area. The original area is unchanged.
        """
        new_area = self.clone()
        for row, column, old_state in self:
            if old_state == CellState.FLOOR:
                continue

            adjacent_coords = [
                (row - 1, column - 1), (row - 1, column), (row - 1, column + 1),  # noqa: E501
                (row,     column - 1),                    (row,     column + 1),  # noqa: E501
                (row + 1, column - 1), (row + 1, column), (row + 1, column + 1),  # noqa: E501
            ]
            adj_occupied_count = 0
            for adj_row, adj_col in adjacent_coords:
                if self.get(adj_row, adj_col) == CellState.SEAT_OCCUPIED:
                    adj_occupied_count += 1

            if old_state == CellState.SEAT_EMPTY and adj_occupied_count == 0:
                new_state = CellState.SEAT_OCCUPIED
            elif old_state == CellState.SEAT_OCCUPIED and adj_occupied_count >= 4:
                new_state = CellState.SEAT_EMPTY
            else:
                new_state = old_state

            new_area.set(row, column, new_state)

        return new_area

    def get_first_visible_seat(
                self, row: int, column: int, dir: Tuple[int, int],
            ) -> Tuple[int, int, CellState]:
        """
        Returns the row and the column of the first seat visible from
        the given cell in the given direction.

        :param dir: a tuple of row delta and column delta. E.g.:
            (-1, 0) = up
            (-1, 1) = up right
            (0, -1) = left
        """
        dir_row, dir_col = dir
        cur_row = row + dir_row
        cur_col = column + dir_col

        while True:
            cur_state = self.get(cur_row, cur_col)

            if cur_state != CellState.FLOOR or cur_state is None:
                break

            cur_row += dir_row
            cur_col += dir_col

        return cur_row, cur_col, cur_state

    def step2(self) -> 'Area':
        """
        Advances the waiting area state by one step using the second algorithm.
        Returns the updated area. The original area is unchanged.
        """
        new_area = self.clone()
        for row, column, old_state in self:
            if old_state == CellState.FLOOR:
                continue

            dirs = [
                (-1, -1), (-1, 0), (-1, +1),
                (0,  -1),          (0,  +1),
                (+1, -1), (+1, 0), (+1, +1),
            ]
            adj_occupied_count = 0
            for dir in dirs:
                _, _, first_vis_seat = self.get_first_visible_seat(row, column, dir)
                if first_vis_seat == CellState.SEAT_OCCUPIED:
                    adj_occupied_count += 1

            if old_state == CellState.SEAT_EMPTY and adj_occupied_count == 0:
                new_state = CellState.SEAT_OCCUPIED
            elif old_state == CellState.SEAT_OCCUPIED and adj_occupied_count >= 5:
                new_state = CellState.SEAT_EMPTY
            else:
                new_state = old_state

            new_area.set(row, column, new_state)

        return new_area

    def diff(self, other: 'Area') -> List[Tuple[int, int]]:
        """
        Returns a list of coordinates of the cells which are different between
        this area and the other area.

        Assumes both areas are of the same size.
        """
        diff = []
        for row_ix, col_ix, self_state in self:
            other_state = other.get(row_ix, col_ix)
            if self_state != other_state:
                diff.append((row_ix, col_ix))

        return diff


def parse_area(input: str) -> Area:
    area = Area()

    lines = input.strip().split('\n')
    for row_index, line in enumerate(lines):
        for column_index, char in enumerate(line):
            if char == '.':
                state = CellState.FLOOR
            elif char == 'L':
                state = CellState.SEAT_EMPTY
            elif char == '#':
                state = CellState.SEAT_OCCUPIED
            else:
                raise ValueError(
                    f"Invalid cell at row {row_index} "
                    f"column {column_index}: {char!r}")

            area.set(row_index, column_index, state)

    return area


def format_area(area: Area) -> str:
    output = ""

    for row_index in range(area.get_max_row_index() + 1):
        for column_index in range(area.get_max_column_index() + 1):
            state = area.get(row_index, column_index)
            if state == CellState.FLOOR:
                output += '.'
            elif state == CellState.SEAT_EMPTY:
                output += 'L'
            elif state == CellState.SEAT_OCCUPIED:
                output += '#'
            else:
                raise ValueError(
                    f"Cannot format cell state at row {row_index} "
                    f"column {column_index}: {state!r}")

        output += '\n'

    return output


def count_occupied_seats(area: Area) -> int:
    count = 0
    for row_ix, col_ix, state in area:
        if state == CellState.SEAT_OCCUPIED:
            count += 1
    return count


def advance_until_stable(area: Area) -> Area:
    """
    Evolves the area (using Area.step) until it stops changing.
    """
    while True:
        new_area = area.step()
        if len(new_area.diff(area)) == 0:
            return new_area

        area = new_area


def advance_until_stable2(area: Area) -> Area:
    """
    Evolves the area (using Area.step2) until it stops changing.
    """
    while True:
        new_area = area.step2()
        if len(new_area.diff(area)) == 0:
            return new_area

        area = new_area


def main():
    with open('./input.txt') as f:
        area = parse_area(f.read())

    final_area = advance_until_stable(area)
    final_occ_seats = count_occupied_seats(final_area)
    print(f"Occupied seats: {final_occ_seats}")

    final_area = advance_until_stable2(area)
    final_occ_seats = count_occupied_seats(final_area)
    print(f"Occupied seats (part 2): {final_occ_seats}")


if __name__ == "__main__":
    main()
