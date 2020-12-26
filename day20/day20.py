import re
from dataclasses import dataclass, field
from typing import Dict, Iterable, Iterator, List, Optional, Set, Tuple


@dataclass(frozen=True)
class TileContent:
    """
    The content (the bitmap image) of a single tile.
    The tile's number is out of scope of this class, whether the tile has it or not.
    """
    # The list of tile rows. Each row is a string of "#" and ".".
    content: Tuple[str]

    def __post_init__(self):
        object.__setattr__(self, 'content', tuple(self.content))

    @property
    def top_edge(self) -> str:
        """
        Returns the top edge of the tile as a string from left to right.
        """
        return self.content[0]

    @property
    def bottom_edge(self) -> str:
        """
        Returns the bottom edge of the tile as a string from left to right.
        """
        return self.content[-1]

    @property
    def left_edge(self) -> str:
        """
        Returns the left edge of the tile as a string from top to bottom.
        """
        return ''.join(row[0] for row in self.content)

    @property
    def right_edge(self) -> str:
        """
        Returns the right edge of the tile as a string from top to bottom..
        """
        return ''.join(row[-1] for row in self.content)

    def mirror_h(self) -> 'TileContent':
        """
        Returns a new tile with content mirrored along the vertical axis.
        """
        mirrored_content = []
        for row in self.content:
            mirrored_content.append(''.join(reversed(row)))
        return TileContent(tuple(mirrored_content))

    def rotate_cw(self) -> 'TileContent':
        """
        Returns a new tile with content rotated clock-wise by 90 degrees.
        """
        rotated_content = []
        for row_split in zip(*self.content):
            row = ''.join(reversed(row_split))
            rotated_content.append(row)
        return TileContent(tuple(rotated_content))

    def strip_edges(self) -> 'TileContent':
        """
        Returns a new tile with all four edges removed.
        """
        stripped_content = []
        for row in self.content[1:-1]:
            stripped_content.append(row[1:-1])
        return TileContent(tuple(stripped_content))

    def concat_right(self, tile: 'TileContent') -> 'TileContent':
        """
        Combines content of this tile and the given tile by concatenating
        the second to the right edge of the first.
        Returns the new tile content.
        """
        combined_content = []
        for left_row, right_row in zip(self.content, tile.content):
            combined_content.append(left_row + right_row)
        return TileContent(tuple(combined_content))

    def concat_bottom(self, tile: 'TileContent') -> 'TileContent':
        """
        Combines content of this tile and the given tile by concatenating
        the second to the bottom edge of the first.
        Returns the new tile content.
        """
        return TileContent(tuple([*self.content, *tile.content]))


def parse_tile(content: str) -> Tuple[int, TileContent]:
    """
    Parses textual representation of a tile.

    :param content: Example::

        Tile 2311:
        ..##.#..#.
        ##..#.....
        #...##..#.
        ####.#...#
        ##.##.###.
        ##...#.###
        .#.#.#..##
        ..#....#..
        ###...#.#.
        ..###..###

    :returns: The parsed tile number and its content.
    """
    content_lines = content.splitlines()

    header = content_lines[0]
    match = re.compile(r"^Tile (\d+):$").match(header)
    if not match:
        raise ValueError(f"Invalid tile header: {header!r}")

    number = int(match.group(1))

    tile_lines = content_lines[1:]

    return number, TileContent(tile_lines)


def read_tiles(path: str) -> Dict[int, TileContent]:
    """
    Opens the file and reads tiles from it using parse_tile.
    Each tile must be separated from other by an empty line.

    :returns: A dictionary that maps each tile's number to its content.
    """
    with open(path) as f:
        tile_texts = f.read().split('\n\n')
        tiles = {}
        for tile_text in tile_texts:
            number, content = parse_tile(tile_text)
            tiles[number] = content

    return tiles


def iter_tile_variations(c: TileContent) -> Iterator[TileContent]:
    """
    Given a tile content iterates over all 8 possible transformations of it
    after a combination of rotations and mirroring.

    Yields the original tile among the variations too.
    """
    yield c
    c = c.rotate_cw()
    yield c
    c = c.rotate_cw()
    yield c
    c = c.rotate_cw()
    yield c
    c = c.rotate_cw()

    c = c.mirror_h()
    yield c
    c = c.rotate_cw()
    yield c
    c = c.rotate_cw()
    yield c
    c = c.rotate_cw()
    yield c


@dataclass
class EdgeIndex:
    """
    A utilitary class which optimizes searching for matching tiles.

    Provides a way to index tiles by the edges of all their variations (see iter_tile_variations)
    and methods to search for a tile variation by one of its edges.
    """
    _all: Set[Tuple[int, TileContent]] = field(default_factory=set)
    _top_edges: Dict[str, Set[Tuple[int, TileContent]]] = field(default_factory=dict)
    _bottom_edges: Dict[str, Set[Tuple[int, TileContent]]] = field(default_factory=dict)
    _left_edges: Dict[str, Set[Tuple[int, TileContent]]] = field(default_factory=dict)
    _right_edges: Dict[str, Set[Tuple[int, TileContent]]] = field(default_factory=dict)

    def add(self, tile_number: int, tile_content: TileContent):
        """
        Adds all variations of this tile to the index.
        """
        for variation in iter_tile_variations(tile_content):
            self._all.add((tile_number, variation))
            self._top_edges.setdefault(variation.top_edge, set()).add((tile_number, variation))
            self._bottom_edges.setdefault(variation.bottom_edge, set()).add((tile_number, variation))
            self._left_edges.setdefault(variation.left_edge, set()).add((tile_number, variation))
            self._right_edges.setdefault(variation.right_edge, set()).add((tile_number, variation))

    def all(self) -> Set[Tuple[int, TileContent]]:
        """
        Returns a set of all possible tile variations in the index.

        :returns: A set of tuples. Each tuple contains a tile's number and its content.
        """
        return self.find()

    def find(
                self,
                top_edge: Optional[str] = None,
                bottom_edge: Optional[str] = None,
                left_edge: Optional[str] = None,
                right_edge: Optional[str] = None,
            ) -> Set[Tuple[int, TileContent]]:
        """
        Returns a set of tile variations which have specified edges.
        Each of the four params is optional and restricts the results by a given edge.
        So, to find tiles with the given top edge, call::

            edge_index.find(top_edge='#.#...')

        To find tiles with the given top edge AND the left edge, call::

            edge_index.find(top_edge='#.#...', left_edge='#...##')

        Without any params a call to .find() is equivalent to a call to .all().

        :returns:  A set of tuples. Each tuple contains a tile's number and its content.
        """
        results = None

        if top_edge:
            top_edge_results = self._top_edges[top_edge]
            results = results & top_edge_results if results else set(top_edge_results)

        if bottom_edge:
            bottom_edge_results = self._bottom_edges[bottom_edge]
            results = results & bottom_edge_results if results else set(bottom_edge_results)

        if left_edge:
            left_edge_results = self._left_edges[left_edge]
            results = results & left_edge_results if results else set(left_edge_results)

        if right_edge:
            right_edge_results = self._right_edges[right_edge]
            results = results & right_edge_results if results else set(right_edge_results)

        if results is None:
            return set(self._all)
        else:
            return results


def index_edges(tiles: Dict[int, TileContent]) -> EdgeIndex:
    """
    Constructs an EdgeIndex from given tiles.

    :param tiles: A dict that maps a tile's number to its content.
    """
    index = EdgeIndex()

    for number, tile_content in tiles.items():
        index.add(number, tile_content)

    return index


def _iter_solution_rows(
            width: int,
            edge_index: EdgeIndex,
            left_edge: Optional[str] = None,
            top_edges: Optional[List[str]] = None,
            exclude_tiles: Optional[Iterable[int]] = None,
        ) -> Iterator[List[Tuple[int, TileContent]]]:
    """
    Iterates over all possible rows of tiles from the edge_index of given width (i.e. length)
    matching the given contraints on the edges.

    :param width: The required length of the row.
    :param edge_index: The index to be used to look up tiles in.
    :param left_edge: Optional requirement for the left-most edge of the row.
        If it's passed, the function will only yield rows whose first tile has the given left edge.
    :param top_edges: Optional requirement for the top-most edges of the row.
        Specifies the top edge for each tile in the row. The len(top_edges) must be equal
        to the row's width.
    :param exclude_tiles: Optional enumeration of tile numbers which should not be included
        in the row.

    :returns: An iteration over rows. Each row is a list of two-element tuples.
        Each tuple contain the tile's number and the content of its variation.
        Each pair of subsequent tiles will have matching touching edges (right edge
        of the former tile will be equal to the left edge of the later tile).
    """
    if width == 0:
        yield []

    exclude_tiles = exclude_tiles or set()

    if left_edge and top_edges:
        leftmost_tiles = edge_index.find(left_edge=left_edge, top_edge=top_edges[0])
    elif left_edge:
        leftmost_tiles = edge_index.find(left_edge=left_edge)
    elif top_edges:
        leftmost_tiles = edge_index.find(top_edge=top_edges[0])
    else:
        leftmost_tiles = edge_index.all()

    for tile_number, tile_content in leftmost_tiles:
        if tile_number in exclude_tiles:
            continue

        subrows = _iter_solution_rows(
            width=width-1,
            edge_index=edge_index,
            left_edge=tile_content.right_edge,
            top_edges=top_edges[1:] if top_edges else None,
            exclude_tiles={*exclude_tiles, tile_number},
        )
        for subrow in subrows:
            yield [(tile_number, tile_content), *subrow]


class NoSolutionError(Exception):
    pass


def _find_solution_tiles(
            width: int,
            height: int,
            edge_index: EdgeIndex,
            top_edges: Optional[List[str]] = None,
            exclude_tiles: Optional[Iterable[int]] = None,
        ) -> List[List[Tuple[int, TileContent]]]:
    """
    Finds the matching grid of tiles. In the found 2d grid all touching tile
    edges are equal.

    :param width: The width of the grid in tiles.
    :param height: The height of the grid in tiles.
    :param edge_index: The index to use to look up tiles in.
    :param top_edges: Optional requirement for the top-most edges of the grid.
        Specifies the top edge for each tile in the first row. The len(top_edges) must be equal
        to the grid's width.
    :param exclude_tiles: Optional enumeration of tile numbers which should not be included
        in the grid.

    :returns: The grid in the form of a list of rows. Each row is a list of two-element tuples.
        Each tuple contain the tile's number and the content of its variation.

    :raises NoSolutionError: If there is no possible grid.
    """
    if height == 0:
        return []

    exclude_tiles = exclude_tiles or set()

    first_rows = _iter_solution_rows(
        width=width,
        edge_index=edge_index,
        top_edges=top_edges,
        exclude_tiles=exclude_tiles,
    )
    for first_row in first_rows:
        try:
            subsolution = _find_solution_tiles(
                width=width,
                height=height-1,
                edge_index=edge_index,
                top_edges=[content.bottom_edge for number, content in first_row],
                exclude_tiles={*exclude_tiles, *(number for number, content in first_row)},
            )
            return [first_row, *subsolution]
        except NoSolutionError:
            continue

    raise NoSolutionError("No solution to this one")


@dataclass
class Solution:
    """
    A helper structure for a 2d grid of matching tiles.
    In the grid all touching tile edges are equal.

    :ivar width: The width of the grid in tiles.
    :ivar height: The height of the grid in tiles.
    :ivar tiles: The grid in the form of a list of rows. Each row is a list of two-element tuples.
        Each tuple contain the tile's number and the content of its variation.
    """
    width: int
    height: int
    tiles: List[List[Tuple[int, TileContent]]]

    @property
    def corner_tile_numbers(self) -> List[int]:
        """
        Returns the tile numbers of corners of the grid in order:
        top-left, top-right, bottom-right, bottom-left.
        """
        return [
            self.tiles[0][0][0],
            self.tiles[0][-1][0],
            self.tiles[-1][-1][0],
            self.tiles[-1][0][0],
        ]


def arrange_tiles(width: int, height: int, tiles: Dict[int, TileContent]) -> Solution:
    """
    Finds the matching grid of tiles. In the found 2d grid all touching tile
    edges are equal.

    :param width: The width of the grid in tiles.
    :param height: The height of the grid in tiles.
    :param tiles: A dict that maps a tile's number to its content.
    """
    tiles = _find_solution_tiles(
        width=width,
        height=height,
        edge_index=index_edges(tiles),
    )
    return Solution(width=width, height=height, tiles=tiles)


def format_solution(solution: Solution) -> str:
    """
    Formats the grid of tiles into a graphical string contains the tile's numbers
    and their content.

    Example of the output::

        12   46
        #.#. .##.
        #..# ##..
        #### ###.
        #... .##.

        83   90
        #... .###
        ..## #..#
        .... ...#
        ##.. ....
    """
    if not solution.tiles or not solution.tiles[0]:
        return ""

    tile_size = len(solution.tiles[0][0][1].content)

    formatted = ""
    for solution_row in solution.tiles:
        for number, _ in solution_row:
            formatted += str(number).ljust(tile_size)
            formatted += " "
        formatted += "\n"

        for tile_row_index in range(tile_size):
            for _, tile_content in solution_row:
                formatted += tile_content.content[tile_row_index]
                formatted += " "
            formatted += "\n"
        formatted += "\n"
    return formatted


def into_one_tile_image(solution: Solution) -> TileContent:
    """
    Combines the grid of tiles into one big tile.
    The edges of each tile are stripped before concatenation using TileContent.strip_edges.
    """
    row_tiles: List[TileContent] = []
    for row in solution.tiles:
        row_tile = row[0][1].strip_edges()
        for number, tile_content in row[1:]:
            row_tile = row_tile.concat_right(tile_content.strip_edges())
        row_tiles.append(row_tile)

    image_tile = row_tiles[0]
    for row_tile in row_tiles[1:]:
        image_tile = image_tile.concat_bottom(row_tile)

    return image_tile


@dataclass
class LookupImage:
    """
    A class for a bitmap image useful to quickly look up bits by its coordinates.

    :ivar width: The width of the image in bits.
    :ivar height: The height of the image in bits.
    :ivar set_pixels: The set of coordinates of set bits/pixels.
        Each element of the set if a tuple of (row, column) zero-based coordinates.
    """
    width: int
    height: int
    set_pixels: Set[Tuple[int, int]] = field(default_factory=set)


def into_lookup_image(tile: TileContent) -> LookupImage:
    """
    Converts a tile into a LookupImage.
    """
    height = len(tile.content)
    width = len(tile.content[0]) if height else 0
    set_pixels = set()
    for row_index, row in enumerate(tile.content):
        for pixel_index, pixel in enumerate(row):
            if pixel == '#':
                set_pixels.add((row_index, pixel_index))
    return LookupImage(width, height, set_pixels)


def get_sea_monster_pattern_pixels() -> Set[Tuple[int, int]]:
    """
    Returns coordinates of bits in the sea monster pattern given that the top-left
    pixel of the pattern has coordinates of (0, 0).

    :returns: A set of tuples. Each tuples is coordinates of a set pixel
        in the form (row, column).
    """
    PATTERN = [
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   ",
    ]
    pixels = set()
    for row_index, row in enumerate(PATTERN):
        for pixel_index, pixel in enumerate(row):
            if pixel == '#':
                pixels.add((row_index, pixel_index))
    return pixels


def locate_sea_monster(image: LookupImage, row: int, column: int) -> Optional[Set[Tuple[int, int]]]:
    """
    Checks if the image contains a sea monster pattern at the given location.

    :param image: The image too look for sea monsters in.
    :param row: The zero-based row number of the top-left corner of the sea monster pattern.
    :param column: The zero-based column number of the top-left corner of the sea monster pattern.

    :returns: None if the image contains no sea monster in this place.
        If it does, returns the set of coordinates pixels of the pattern, which can be
        useful to count how many pixels the sea monster occupies.
    """
    monster_pixels = set()
    for pattern_row, pattern_col in get_sea_monster_pattern_pixels():
        target_pixel = (row + pattern_row, column + pattern_col)
        if target_pixel not in image.set_pixels:
            return None

        monster_pixels.add(target_pixel)

    return monster_pixels


def _find_sea_monsters_image(image: LookupImage) -> Tuple[int, Set[Tuple[int, int]]]:
    """
    Finds all sea monsters in the image.

    :returns: A tuple of two values.
        The first value is the number of found monsters.
        The second value is the set of coordinats of pixels occupied by the found monsters.
    """
    found_monsters = 0
    monster_pixels = set()
    for row_ix in range(image.height):
        for column_ix in range(image.width):
            loc_monster_pixels = locate_sea_monster(image, row_ix, column_ix)
            if loc_monster_pixels:
                found_monsters += 1
                monster_pixels |= loc_monster_pixels

    return found_monsters, monster_pixels


def find_sea_monsters(tile: TileContent) -> Tuple[int, Set[Tuple[int, int]]]:
    """
    Finds all sea monsters in the tile. Rotates and mirrors the tile until the maximum
    number of monsters is found.

    :returns: A tuple of two values.
        The first value is the number of found monsters.
        The second value is the set of coordinats of pixels occupied by the found monsters.
    """
    found_monsters = 0
    monster_pixels = set()
    for variation in iter_tile_variations(tile):
        var_found_monsters, var_monster_pixels = _find_sea_monsters_image(into_lookup_image(variation))
        if var_found_monsters > found_monsters:
            found_monsters = var_found_monsters
            monster_pixels = var_monster_pixels

    return found_monsters, monster_pixels


def main():
    tiles = read_tiles('./input.txt')

    solution = arrange_tiles(12, 12, tiles)
    print(format_solution(solution))

    corner_product = 1
    for corner_number in solution.corner_tile_numbers:
        corner_product *= corner_number
    print(f"Product of corner tile numbers: {corner_product}")

    image_tile = into_one_tile_image(solution)
    found_monsters, monster_pixels = find_sea_monsters(image_tile)
    total_pixels_count = len(into_lookup_image(image_tile).set_pixels)
    print(f"Found monsters: {found_monsters}")
    print(f"Water roughness: {total_pixels_count - len(monster_pixels)}")


if __name__ == "__main__":
    main()
