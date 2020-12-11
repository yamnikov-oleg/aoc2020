from day11 import CellState, advance_until_stable, format_area, parse_area


def test_parse_area():
    input = (
        "L.LL.LL.LL\n"
        "LLLLLLL.LL\n"
        "L.L.L..L..\n"
        "LLLL.LL.LL\n"
        "L.LL.LL.LL\n"
        "L.LLLLL.LL\n"
        "..L.L.....\n"
        "LLLLLLLLLL\n"
        "L.LLLLLL.L\n"
        "L.LLLLL.L#\n"
    )
    area = parse_area(input)

    # I'll just check several points
    assert area.get(0, 0) == CellState.SEAT_EMPTY
    assert area.get(0, 9) == CellState.SEAT_EMPTY
    assert area.get(0, 9) == CellState.SEAT_EMPTY
    assert area.get(9, 9) == CellState.SEAT_OCCUPIED
    assert area.get(2, 3) == CellState.FLOOR


def test_area_get():
    input = (
        "L.LL.LL.LL\n"
        "LLLLLLL.LL\n"
        "L.L.L..L..\n"
        "LLLL.LL.LL\n"
        "L.LL.LL.LL\n"
        "L.LLLLL.LL\n"
        "..L.L.....\n"
        "LLLLLLLLLL\n"
        "L.LLLLLL.L\n"
        "L.LLLLL.LL\n"
    )
    area = parse_area(input)

    assert area.get(0, 0) == CellState.SEAT_EMPTY
    assert area.get(-1, 0) is None
    assert area.get(0, -1) is None
    assert area.get(10, 0) is None
    assert area.get(0, 10) is None


def test_area_clone():
    area = parse_area(
        "L.LL.LL.LL\n"
        "LLLLLLL.LL\n"
        "L.L.L..L..\n"
        "LLLL.LL.LL\n"
        "L.LL.LL.LL\n"
        "L.LLLLL.LL\n"
        "..L.L.....\n"
        "LLLLLLLLLL\n"
        "L.LLLLLL.L\n"
        "L.LLLLL.LL\n"
    )
    assert area.get(0, 0) == CellState.SEAT_EMPTY

    clone = area.clone()
    clone.set(0, 0, CellState.SEAT_OCCUPIED)
    assert clone.get(0, 0) == CellState.SEAT_OCCUPIED

    # Unchanged
    assert area.get(0, 0) == CellState.SEAT_EMPTY


def test_area_step():
    area = parse_area(
        "L.LL.LL.LL\n"
        "LLLLLLL.LL\n"
        "L.L.L..L..\n"
        "LLLL.LL.LL\n"
        "L.LL.LL.LL\n"
        "L.LLLLL.LL\n"
        "..L.L.....\n"
        "LLLLLLLLLL\n"
        "L.LLLLLL.L\n"
        "L.LLLLL.LL\n"
    )

    area = area.step()
    assert format_area(area) == (
        "#.##.##.##\n"
        "#######.##\n"
        "#.#.#..#..\n"
        "####.##.##\n"
        "#.##.##.##\n"
        "#.#####.##\n"
        "..#.#.....\n"
        "##########\n"
        "#.######.#\n"
        "#.#####.##\n"
    )

    area = area.step()
    assert format_area(area) == (
        "#.LL.L#.##\n"
        "#LLLLLL.L#\n"
        "L.L.L..L..\n"
        "#LLL.LL.L#\n"
        "#.LL.LL.LL\n"
        "#.LLLL#.##\n"
        "..L.L.....\n"
        "#LLLLLLLL#\n"
        "#.LLLLLL.L\n"
        "#.#LLLL.##\n"
    )


def test_area_diff():
    area1 = parse_area(
        "L.LL.LL.LL\n"
        "LLLLLLL.LL\n"
        "L.L.L..L..\n"
        "LLLL.LL.LL\n"
        "L.LL.LL.LL\n"
        "L.LLLLL.LL\n"
        "..L.L.....\n"
        "LLLLLLLLLL\n"
        "L.LLLLLL.L\n"
        "L.LLLLL.LL\n"
    )
    area2 = parse_area(
        "#.##.##.##\n"
        "#######.##\n"
        "#.#.#..#..\n"
        "####.##.##\n"
        "#.##.##.##\n"
        "#.#####.##\n"
        "..#.#.....\n"
        "##########\n"
        "#.######.#\n"
        "#.#####.##\n"
    )
    assert len(area1.diff(area2)) == 71

    area1 = parse_area(
        "#.#L.L#.##\n"
        "#LLL#LL.L#\n"
        "L.#.L..#..\n"
        "#L##.##.L#\n"
        "#.#L.LL.LL\n"
        "#.#L#L#.##\n"
        "..L.L.....\n"
        "#L#L##L#L#\n"
        "#.LLLLLL.L\n"
        "#.#L#L#.##\n"
    )
    area2 = parse_area(
        "#.#L.L#.##\n"
        "#LLL#LL.L#\n"
        "L.#.L..#..\n"
        "#L##.##.L#\n"
        "#.#L.LL.LL\n"
        "#.#L#L#.##\n"
        "..L.L.....\n"
        "#L#L##L#L#\n"
        "#.LLLLLL.L\n"
        "#.#L#L#.##\n"
    )
    assert len(area1.diff(area2)) == 0


def test_advance_until_stable():
    area = parse_area(
        "L.LL.LL.LL\n"
        "LLLLLLL.LL\n"
        "L.L.L..L..\n"
        "LLLL.LL.LL\n"
        "L.LL.LL.LL\n"
        "L.LLLLL.LL\n"
        "..L.L.....\n"
        "LLLLLLLLLL\n"
        "L.LLLLLL.L\n"
        "L.LLLLL.LL\n"
    )
    area = advance_until_stable(area)
    assert format_area(area) == (
        "#.#L.L#.##\n"
        "#LLL#LL.L#\n"
        "L.#.L..#..\n"
        "#L##.##.L#\n"
        "#.#L.LL.LL\n"
        "#.#L#L#.##\n"
        "..L.L.....\n"
        "#L#L##L#L#\n"
        "#.LLLLLL.L\n"
        "#.#L#L#.##\n"
    )
