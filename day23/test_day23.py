from day23 import parse_cup_circle


def test_cup_circle_play_round():
    circle = parse_cup_circle("389125467")

    for i in range(10):
        circle.play_round()
    assert circle.cups.to_list() == [8, 3,  7,  4,  1,  9,  2,  6, 5]

    for i in range(90):
        circle.play_round()
    assert circle.get_part1_answer() == "67384529"


def test_cup_circle_play_10m_rounds():
    circle = parse_cup_circle("389125467")
    circle.expand_to(1_000_000)

    for i in range(10_000_000):
        circle.play_round()
    assert circle.get_part2_answer() == 149245887792
