from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class Bus:
    is_in_service: bool
    # For buses out of service id is None.
    id: Optional[int] = None


def parse_buses(line: str) -> List[Bus]:
    buses = []
    id_strs = line.strip().split(',')
    for id_str in id_strs:
        if id_str == 'x':
            buses.append(Bus(is_in_service=False))
        else:
            buses.append(Bus(is_in_service=True, id=int(id_str)))

    return buses


def find_next_bus(buses: List[Bus], time: int) -> Tuple[int, Bus]:
    """
    Returns the timestamp when the next bus departs after the time
    and the bus itself.
    """
    # Each tuple contains the timestamp of the next departure
    # of the bus after the `time` and the bus itself.
    bus_departures: List[Tuple[int, Bus]] = []
    for bus in buses:
        if not bus.is_in_service:
            continue

        if (time % bus.id) == 0:
            departure = time
        else:
            departure = (time // bus.id + 1) * bus.id

        bus_departures.append((departure, bus))

    return min(bus_departures, key=lambda db: db[0])


def main():
    with open('./input.txt') as f:
        lines = f.readlines()
        departure_time_after = int(lines[0].strip())
        buses = parse_buses(lines[1])

    departure_time, next_bus = find_next_bus(buses, departure_time_after)
    print(f"The next bus is {next_bus.id}, departs at {departure_time}")
    print(f"Part 1 answer: {(departure_time - departure_time_after) * next_bus.id}")


if __name__ == "__main__":
    main()
