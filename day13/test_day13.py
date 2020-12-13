from day13 import find_magic_departure_time, parse_buses


def test_find_magic_departure_time():
    assert find_magic_departure_time(parse_buses("7,13,x,x,59,x,31,19")) == 1068781
    assert find_magic_departure_time(parse_buses("17,x,13,19")) == 3417
    assert find_magic_departure_time(parse_buses("67,7,59,61")) == 754018
    assert find_magic_departure_time(parse_buses("67,x,7,59,61")) == 779210
    assert find_magic_departure_time(parse_buses("67,7,x,59,61")) == 1261476
    assert find_magic_departure_time(parse_buses("1789,37,47,1889")) == 1202161486
