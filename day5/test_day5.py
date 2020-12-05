from day5 import decode_seat, Seat


def test_decode_seat():
    assert decode_seat("FBFBBFFRLR") == Seat(row=44, column=5)
    assert decode_seat("BFFFBBFRRR") == Seat(row=70, column=7)
    assert decode_seat("FFFBBBFRRR") == Seat(row=14, column=7)
    assert decode_seat("BBFFBBFRLL") == Seat(row=102, column=4)
