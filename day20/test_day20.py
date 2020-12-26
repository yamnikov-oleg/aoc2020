import pytest

from day20 import (Solution, TileContent, arrange_tiles, find_sea_monsters,
                   format_solution, into_one_tile_image, parse_tile,
                   read_tiles)


@pytest.mark.parametrize("content, number, tile_content", [
    (
        (
            "Tile 2311:\n"
            "..##.#..#.\n"
            "##..#.....\n"
            "#...##..#.\n"
            "####.#...#\n"
            "##.##.###.\n"
            "##...#.###\n"
            ".#.#.#..##\n"
            "..#....#..\n"
            "###...#.#.\n"
            "..###..###\n"
        ),
        2311,
        TileContent([
            "..##.#..#.",
            "##..#.....",
            "#...##..#.",
            "####.#...#",
            "##.##.###.",
            "##...#.###",
            ".#.#.#..##",
            "..#....#..",
            "###...#.#.",
            "..###..###",
        ]),
    ),
])
def test_parse_tile(content, number, tile_content):
    assert parse_tile(content) == (number, tile_content)


def test_arrange_tiles():
    tiles = read_tiles('./test.txt')
    expected_solution = Solution(
        width=3,
        height=3,
        tiles=[
            [
                (1951, TileContent([
                    "#...##.#..",
                    "..#.#..#.#",
                    ".###....#.",
                    "###.##.##.",
                    ".###.#####",
                    ".##.#....#",
                    "#...######",
                    ".....#..##",
                    "#.####...#",
                    "#.##...##.",
                ])),
                (2311, TileContent([
                    "..###..###",
                    "###...#.#.",
                    "..#....#..",
                    ".#.#.#..##",
                    "##...#.###",
                    "##.##.###.",
                    "####.#...#",
                    "#...##..#.",
                    "##..#.....",
                    "..##.#..#.",
                ])),
                (3079, TileContent([
                    "#.#.#####.",
                    ".#..######",
                    "..#.......",
                    "######....",
                    "####.#..#.",
                    ".#...#.##.",
                    "#.#####.##",
                    "..#.###...",
                    "..#.......",
                    "..#.###...",
                ])),
            ],
            [
                (2729, TileContent([
                    "#.##...##.",
                    "##..#.##..",
                    "##.####...",
                    "####.#.#..",
                    ".#.####...",
                    ".##..##.#.",
                    "....#..#.#",
                    "..#.#.....",
                    "####.#....",
                    "...#.#.#.#",
                ])),
                (1427, TileContent([
                    "..##.#..#.",
                    "..#..###.#",
                    ".#.####.#.",
                    "...#.#####",
                    "...##..##.",
                    "....#...##",
                    "#.#.#.##.#",
                    ".#.##.#..#",
                    ".#..#.##..",
                    "###.##.#..",
                ])),
                (2473, TileContent([
                    "..#.###...",
                    "##.##....#",
                    "..#.###..#",
                    "###.#..###",
                    ".######.##",
                    "#.#.#.#...",
                    "#.###.###.",
                    "#.###.##..",
                    ".######...",
                    ".##...####",
                ])),
            ],
            [
                (2971, TileContent([
                    "...#.#.#.#",
                    "..#.#.###.",
                    "..####.###",
                    "#..#.#..#.",
                    ".#..####.#",
                    ".#####..##",
                    "##.##..#..",
                    "#.#.###...",
                    "#...###...",
                    "..#.#....#",
                ])),
                (1489, TileContent([
                    "###.##.#..",
                    "..##.##.##",
                    "##.#...##.",
                    "...#.#.#..",
                    "#..#.#.#.#",
                    "#####...#.",
                    "..#...#...",
                    ".##..##...",
                    "..##...#..",
                    "##.#.#....",
                ])),
                (1171, TileContent([
                    ".##...####",
                    "#..#.##..#",
                    ".#.#..#.##",
                    ".####.###.",
                    "####.###..",
                    ".##....##.",
                    ".####...#.",
                    ".####.##.#",
                    "...#..####",
                    "...##.....",
                ])),
            ],
        ]
    )

    found_solution = arrange_tiles(3, 3, tiles)
    print(format_solution(found_solution))

    assert set(found_solution.corner_tile_numbers) == set(expected_solution.corner_tile_numbers)


def test_find_sea_monsters():
    tiles = read_tiles('./test.txt')
    solution = arrange_tiles(3, 3, tiles)
    found_monsters, monster_pixels = find_sea_monsters(into_one_tile_image(solution))
    assert found_monsters == 2
    assert len(monster_pixels) == 30
