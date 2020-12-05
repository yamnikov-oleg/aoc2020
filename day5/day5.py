from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class Seat:
    row: int
    column: int

    @property
    def id(self):
        return self.row * 8 + self.column


def decode_binary(encoded: str, lower: str, upper: str) -> int:
    decoded = 0
    while encoded:
        digit = encoded[0]
        encoded = encoded[1:]

        if digit == lower:
            decoded = decoded * 2
        elif digit == upper:
            decoded = decoded * 2 + 1
        else:
            raise ValueError(f"Invalid digit: {digit:!r}")

    return decoded


def decode_seat(bsp: str) -> Seat:
    row = decode_binary(bsp[0:7], lower='F', upper='B')
    column = decode_binary(bsp[7:10], lower='L', upper='R')
    return Seat(row=row, column=column)


def find_missing_seats(seats: List[Seat]) -> List[Seat]:
    min_row = min([s.row for s in seats])
    max_row = max([s.row for s in seats])

    min_column = min([s.column for s in seats])
    max_column = max([s.column for s in seats])

    seat_map: Dict[Tuple[int, int]] = {}
    for seat in seats:
        seat_map[(seat.row, seat.column)] = seat

    missing_seats: List[Seat] = []
    for row in range(min_row, max_row + 1):
        for column in range(min_column, max_column + 1):
            seat_is_missing = (row, column) not in seat_map
            next_row_seat_is_present = (row + 1, column) in seat_map
            prev_row_seat_is_present = (row - 1, column) in seat_map

            if seat_is_missing and next_row_seat_is_present and prev_row_seat_is_present:
                missing_seats.append(Seat(row=row, column=column))

    return missing_seats


def main():
    with open('./input.txt') as f:
        lines = f.readlines()
        seats = [decode_seat(l) for l in lines]

    max_id_seat = max(seats, key=lambda seat: seat.id)
    print(f"Max ID: {max_id_seat.id}")

    missing_seats = find_missing_seats(seats)
    print("Missing seats:")
    for seat in missing_seats:
        print(f"{seat}: id {seat.id}")


if __name__ == "__main__":
    main()
