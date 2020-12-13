import math
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


def extended_gcd(a, b):
    """
    Extended Greatest Common Divisor Algorithm

    Returns:
        gcd: The greatest common divisor of a and b.
        s, t: Coefficients such that s*a + t*b = gcd

    Reference:
        https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode

    Implementation copied from:
        https://math.stackexchange.com/a/3864593
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        quotient, remainder = divmod(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def lcm(a, b):
    """
    Returns least common multiple of two numbers.
    """
    return abs(a*b) // math.gcd(a, b)


def find_magic_departure_time(buses: List[Bus]) -> int:
    def _find_2_bus(bus1_start, bus1_speed, bus2_speed):
        """
        Given two buses returns such time t so that bus 1 departs at time t and
        bus 2 departs at time t+1.

        :param bus1_start: - time at which bus 1 starts on the route.
        :param bus1_speed: - the period of the bus 1.
        :param bus2_speed: - the period of the bus 2. Bus 2 starts his route
            at time 0.
        """
        gcd, s, t = extended_gcd(bus1_speed, bus2_speed)
        offset = bus1_start + 1

        return (bus1_start - bus1_speed * s * (offset // gcd)) % lcm(bus1_speed, bus2_speed)

    def _find_rec(bus0_start, bus0_speed, buses: List[Bus]) -> int:
        """
        Given a bus 0 and a list of other buses, returns such time t so that
        bus 0 departs at time t, the first bus from the list departs
        at time t+1, and so on.

        :param bus0_start: - time at which bus 0 starts on the route.
        :param bus0_speed: - the period of the bus 0.
        :param buses: - a list of other buses, all of which start their
            movement at time 0.
        """
        if buses[0].is_in_service:
            # Find the time t for the bus 0 and buses[0]
            t = _find_2_bus(bus0_start, bus0_speed, buses[0].id)
            if len(buses) == 1:
                # If this is the last bus - this t is the answer.
                return t
            else:
                # If there're more buses, we do a trick.
                # We imagine that t is the departure time for another,
                # imaginary bus. This imaginary bus departs at time t
                # and returns to this point after the certain period, which
                # is the LCM of speeds of bus 0 and buses[0].
                #
                # This way we reduce our problem from N buses to N-1 buses.
                period = lcm(bus0_speed, buses[0].id)
                return _find_rec(t + 1, period, buses[1:]) - 1
        else:
            if len(buses) == 1:
                # There are no more buses. The departure time of bus 0 is
                # the time t.
                return bus0_start
            else:
                # Ignore this bus since it's out of service and move on.
                # Add 1 to the bus0_start because we still have to count
                # the offset of 1 for this skipped bus.
                return _find_rec(bus0_start + 1, bus0_speed, buses[1:]) - 1

    return _find_rec(0, buses[0].id, buses[1:])


def main():
    with open('./input.txt') as f:
        lines = f.readlines()
        departure_time_after = int(lines[0].strip())
        buses = parse_buses(lines[1])

    departure_time, next_bus = find_next_bus(buses, departure_time_after)
    print(f"The next bus is {next_bus.id}, departs at {departure_time}")
    print(f"Part 1 answer: {(departure_time - departure_time_after) * next_bus.id}")

    magic_time = find_magic_departure_time(buses)
    print(f"Part 2 departure time: {magic_time}")


if __name__ == "__main__":
    main()
