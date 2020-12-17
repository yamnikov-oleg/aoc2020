from day17 import PocketDim, PocketDim4, parse_pocket_dim, parse_pocket_dim4


def test_parse_pocket_dim():
    assert parse_pocket_dim(
        ".#.\n"
        "..#\n"
        "###\n"
    ) == PocketDim(active_cubes={
        (1, 0, 0),
        (2, 1, 0),
        (0, 2, 0),
        (1, 2, 0),
        (2, 2, 0),
    })


def test_pocket_dim_step():
    dim = parse_pocket_dim(
        ".#.\n"
        "..#\n"
        "###\n"
    )

    dim = dim.step()
    assert dim.active_cubes == {
        (0, 1, -1),
        (2, 2, -1),
        (1, 3, -1),
        (0, 1, 0),
        (2, 1, 0),
        (1, 2, 0),
        (2, 2, 0),
        (1, 3, 0),
        (0, 1, 1),
        (2, 2, 1),
        (1, 3, 1),
    }


def test_parse_pocket_dim4():
    assert parse_pocket_dim4(
        ".#.\n"
        "..#\n"
        "###\n"
    ) == PocketDim4(active_cubes={
        (1, 0, 0, 0),
        (2, 1, 0, 0),
        (0, 2, 0, 0),
        (1, 2, 0, 0),
        (2, 2, 0, 0),
    })


def test_pocket_dim4_step():
    dim = parse_pocket_dim4(
        ".#.\n"
        "..#\n"
        "###\n"
    )

    dim = dim.step()

    assert dim.active_cubes == {
        (0, 1, -1, -1),
        (2, 2, -1, -1),
        (1, 3, -1, -1),

        (0, 1, 0, -1),
        (2, 2, 0, -1),
        (1, 3, 0, -1),

        (0, 1, 1, -1),
        (2, 2, 1, -1),
        (1, 3, 1, -1),

        (0, 1, -1, 0),
        (2, 2, -1, 0),
        (1, 3, -1, 0),

        (0, 1, 0, 0),
        (2, 1, 0, 0),
        (1, 2, 0, 0),
        (2, 2, 0, 0),
        (1, 3, 0, 0),

        (0, 1, 1, 0),
        (2, 2, 1, 0),
        (1, 3, 1, 0),

        (0, 1, -1, 1),
        (2, 2, -1, 1),
        (1, 3, -1, 1),

        (0, 1, 0, 1),
        (2, 2, 0, 1),
        (1, 3, 0, 1),

        (0, 1, 1, 1),
        (2, 2, 1, 1),
        (1, 3, 1, 1),
    }
