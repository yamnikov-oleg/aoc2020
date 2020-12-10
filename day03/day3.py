from dataclasses import dataclass
from typing import List


@dataclass
class Coords:
    """
    Zero-based.
    (0, 0) is the starting point.
    Row indices increase to the bottom.
    Column indices increase to the right.
    """
    row: int = 0
    column: int = 0

    def add(self, right: int, down: int) -> 'Coords':
        return Coords(row=self.row + down, column=self.column + right)


@dataclass
class SlopeRow:
    pattern: str

    def is_tree(self, column: int):
        column = column % len(self.pattern)
        return self.pattern[column] == '#'


@dataclass
class SlopeMap:
    rows: List[SlopeRow]

    def is_tree(self, coords: Coords) -> bool:
        if not self.is_in_bounds(coords):
            raise ValueError('out of bounds')

        row = self.rows[coords.row]
        return row.is_tree(coords.column)

    def is_in_bounds(self, coords: Coords) -> bool:
        return coords.row < len(self.rows)


def parse_row(line: str) -> SlopeRow:
    return SlopeRow(pattern=line.strip())


def parse_map(input: str) -> SlopeMap:
    lines = input.split('\n')
    # Strip each lines
    lines = [l.strip() for l in lines]
    # Remove empty lines
    lines = [l for l in lines if l]

    rows = [parse_row(line) for line in lines]
    return SlopeMap(rows=rows)


def count_trees(slope_map: SlopeMap, right: int, down: int) -> int:
    location = Coords(row=0, column=0)
    trees = 0
    while slope_map.is_in_bounds(location):
        if slope_map.is_tree(location):
            trees += 1

        location = location.add(right, down)

    return trees


def main():
    with open('./input.txt') as f:
        slope_map = parse_map(f.read())

    slopes = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]
    slope_trees = []
    for right, down in slopes:
        trees = count_trees(slope_map, right, down)
        slope_trees.append(trees)
        print(f"Right {right}, down {down} = {trees} trees")

    trees_mult = 1
    for trees in slope_trees:
        trees_mult *= trees
    print(f"Multiplication of these: {trees_mult}")


if __name__ == "__main__":
    main()
