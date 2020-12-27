from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Iterator, List, Set


class Dir(Enum):
    NE = 'ne'
    E = 'e'
    SE = 'se'
    SW = 'sw'
    W = 'w'
    NW = 'nw'


@dataclass(frozen=True)
class HexCoords:
    """
    Immutable coodinates on a hexagonal grid.

    Y identifies the row of the hexagon. Every even row is considered to be
    shifted by half of a tile to the right.
    Y increases to the bottom (south).

    X identifies the column of the hexagon as if the row wasn't shifted.
    X increases to the right (east).

    An illustration of how HexCoords work::

        x=1   x=2   x=3   x=4
        y=1   y=1   y=1   y=1

           x=1   x=2   x=3
           y=2   y=2   y=2

        x=1   x=2   x=3   x=4
        y=3   y=3   y=3   x=3

    """
    x: int = 0
    y: int = 0

    def move(self, dir: Dir) -> 'HexCoords':
        """
        Returns a new coordinates objects produced by moving these coordinates
        by 1 hexagon in the given direction.
        """
        if dir == Dir.NE:
            if self.y % 2 == 0:
                return HexCoords(
                    x=self.x+1,
                    y=self.y-1,
                )
            else:
                return HexCoords(
                    x=self.x,
                    y=self.y-1,
                )
        elif dir == Dir.E:
            return HexCoords(
                x=self.x+1,
                y=self.y,
            )
        elif dir == Dir.SE:
            if self.y % 2 == 0:
                return HexCoords(
                    x=self.x+1,
                    y=self.y+1,
                )
            else:
                return HexCoords(
                    x=self.x,
                    y=self.y+1,
                )
        elif dir == Dir.NW:
            if self.y % 2 == 0:
                return HexCoords(
                    x=self.x,
                    y=self.y-1,
                )
            else:
                return HexCoords(
                    x=self.x-1,
                    y=self.y-1,
                )
        elif dir == Dir.W:
            return HexCoords(
                x=self.x-1,
                y=self.y,
            )
        elif dir == Dir.SW:
            if self.y % 2 == 0:
                return HexCoords(
                    x=self.x,
                    y=self.y+1,
                )
            else:
                return HexCoords(
                    x=self.x-1,
                    y=self.y+1,
                )
        else:
            raise ValueError(f"Invalid direction: {dir!r}")


def iter_neighbors(coords: HexCoords) -> Iterator[HexCoords]:
    """
    Iterates over coordinates of hexagons neighboring to the selected hexagon.
    """
    for dir in Dir:
        yield coords.move(dir)


@dataclass
class TileMap:
    """
    A floor of tiles.

    :ivar black_tiles: Set of coordinates of black tiles. All the other tiles
        on this infinite map are considered white.
    """
    black_tiles: Set[HexCoords] = field(default_factory=set)

    def flip(self, c: HexCoords):
        """
        Flips the file selected tile. Makes it white if it's black or makes it
        black if it's white.
        """
        if c in self.black_tiles:
            self.black_tiles.remove(c)
        else:
            self.black_tiles.add(c)

    def evolve(self) -> 'TileMap':
        """
        Evolve the tiled floor by 1 day.
        Returns a new TileMap, keeping this one unchanged.
        """
        new_black_tiles = set()

        blackening_candidates: Dict[HexCoords, int] = defaultdict(int)
        for black_coords in self.black_tiles:
            black_neighbor_count = 0
            for neighbor in iter_neighbors(black_coords):
                if neighbor in self.black_tiles:
                    black_neighbor_count += 1
                else:
                    blackening_candidates[neighbor] += 1

            if black_neighbor_count == 0 or black_neighbor_count > 2:
                # make it white
                pass
            else:
                # keep it black
                new_black_tiles.add(black_coords)

        for white_coords, black_neighbor_count in blackening_candidates.items():
            if black_neighbor_count == 2:
                new_black_tiles.add(white_coords)

        return TileMap(new_black_tiles)


def parse_dirs(line: str) -> List[Dir]:
    if not line:
        return []
    elif line.startswith('ne'):
        return [Dir.NE, *parse_dirs(line[2:])]
    elif line.startswith('e'):
        return [Dir.E, *parse_dirs(line[1:])]
    elif line.startswith('se'):
        return [Dir.SE, *parse_dirs(line[2:])]
    elif line.startswith('sw'):
        return [Dir.SW, *parse_dirs(line[2:])]
    elif line.startswith('w'):
        return [Dir.W, *parse_dirs(line[1:])]
    elif line.startswith('nw'):
        return [Dir.NW, *parse_dirs(line[2:])]
    else:
        raise ValueError(f"Cannot parse: {line!r}")


def dirs_to_hex_coords(dirs: List[Dir]) -> HexCoords:
    """
    Returns the coordinates produced by moving for HexCoords(0, 0)
    to the given directions one by one.
    """
    coords = HexCoords()
    for dir in dirs:
        coords = coords.move(dir)
    return coords


def fill_tile_map(tile_dirs: List[List[Dir]]) -> TileMap:
    """
    Starts with a all-white tile map.

    For each list of directions calculates the tile coordinates using dirs_to_hex_coords
    and flips the tile.

    Returns the resulting tile map.
    """
    tile_map = TileMap()
    for dirs in tile_dirs:
        coords = dirs_to_hex_coords(dirs)
        tile_map.flip(coords)
    return tile_map


def main():
    with open('./input.txt') as f:
        tile_dirs = [parse_dirs(line.strip()) for line in f.readlines() if line]

    tile_map = fill_tile_map(tile_dirs)
    print(f"Black tiles: {len(tile_map.black_tiles)}")

    for i in range(100):
        tile_map = tile_map.evolve()
    print(f"Black tiles after 100 days: {len(tile_map.black_tiles)}")


if __name__ == "__main__":
    main()
