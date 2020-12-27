import pytest

from day24 import Dir, fill_tile_map, parse_dirs


@pytest.mark.parametrize("line, dirs", [
    ("esenee", [Dir.E, Dir.SE, Dir.NE, Dir.E]),
    ("nwwswee", [Dir.NW, Dir.W, Dir.SW, Dir.E, Dir.E]),
])
def test_parse_dirs(line, dirs):
    assert parse_dirs(line) == dirs


def test_fill_tile_map():
    input = [
        "sesenwnenenewseeswwswswwnenewsewsw",
        "neeenesenwnwwswnenewnwwsewnenwseswesw",
        "seswneswswsenwwnwse",
        "nwnwneseeswswnenewneswwnewseswneseene",
        "swweswneswnenwsewnwneneseenw",
        "eesenwseswswnenwswnwnwsewwnwsene",
        "sewnenenenesenwsewnenwwwse",
        "wenwwweseeeweswwwnwwe",
        "wsweesenenewnwwnwsenewsenwwsesesenwne",
        "neeswseenwwswnwswswnw",
        "nenwswwsewswnenenewsenwsenwnesesenew",
        "enewnwewneswsewnwswenweswnenwsenwsw",
        "sweneswneswneneenwnewenewwneswswnese",
        "swwesenesewenwneswnwwneseswwne",
        "enesenwswwswneneswsenwnewswseenwsese",
        "wnwnesenesenenwwnenwsewesewsesesew",
        "nenewswnwewswnenesenwnesewesw",
        "eneswnwswnwsenenwnwnwwseeswneewsenese",
        "neswnwewnwnwseenwseesewsenwsweewe",
        "wseweeenwnesenwwwswnew",
    ]
    tile_dirs = [parse_dirs(dirs) for dirs in input]
    tile_map = fill_tile_map(tile_dirs)
    assert len(tile_map.black_tiles) == 10


def test_tile_map_evolve():
    input = [
        "sesenwnenenewseeswwswswwnenewsewsw",
        "neeenesenwnwwswnenewnwwsewnenwseswesw",
        "seswneswswsenwwnwse",
        "nwnwneseeswswnenewneswwnewseswneseene",
        "swweswneswnenwsewnwneneseenw",
        "eesenwseswswnenwswnwnwsewwnwsene",
        "sewnenenenesenwsewnenwwwse",
        "wenwwweseeeweswwwnwwe",
        "wsweesenenewnwwnwsenewsenwwsesesenwne",
        "neeswseenwwswnwswswnw",
        "nenwswwsewswnenenewsenwsenwnesesenew",
        "enewnwewneswsewnwswenweswnenwsenwsw",
        "sweneswneswneneenwnewenewwneswswnese",
        "swwesenesewenwneswnwwneseswwne",
        "enesenwswwswneneswsenwnewswseenwsese",
        "wnwnesenesenenwwnenwsewesewsesesew",
        "nenewswnwewswnenesenwnesewesw",
        "eneswnwswnwsenenwnwnwwseeswneewsenese",
        "neswnwewnwnwseenwseesewsenwsweewe",
        "wseweeenwnesenwwwswnew",
    ]
    tile_dirs = [parse_dirs(dirs) for dirs in input]
    tile_map = fill_tile_map(tile_dirs)

    tile_map = tile_map.evolve()
    assert len(tile_map.black_tiles) == 15

    tile_map = tile_map.evolve()
    assert len(tile_map.black_tiles) == 12

    tile_map = tile_map.evolve()
    assert len(tile_map.black_tiles) == 25

    tile_map = tile_map.evolve()
    assert len(tile_map.black_tiles) == 14

    for i in range(96):
        tile_map = tile_map.evolve()
    assert len(tile_map.black_tiles) == 2208
