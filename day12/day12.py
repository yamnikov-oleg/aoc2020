from dataclasses import dataclass, replace
from enum import Enum


class CmdCode(Enum):
    N = 'N'
    S = 'S'
    W = 'W'
    E = 'E'
    R = 'R'
    L = 'L'
    F = 'F'


@dataclass
class Command:
    code: CmdCode
    value: int


def parse_command(line: str) -> Command:
    """
    parse_command("R90")  # => Command(code=CmdCode.R, value=90)
    """
    if len(line) < 2:
        raise ValueError("Command should be at least 2 symbols long")

    code = CmdCode(line[0])

    try:
        value = int(line[1:])
    except ValueError:
        raise ValueError(f"Invalid command value: {line[1:]!r}")

    if code in [CmdCode.L, CmdCode.R]:
        if value not in [90, 180, 270]:
            raise ValueError(f"Invalid rotation angle: {value!r}")

    return Command(code, value)


@dataclass
class Ship:
    # Position coordinates
    north: int = 0
    east: int = 0

    # Clock-wise
    # 0 = east
    # 90 = south
    # 180 = west
    # 270 = north
    angle: int = 0


def move_ship(ship: Ship, cmd: Command) -> Ship:
    """
    Calculates the new ship location after execution of the command.
    Returns the new location, the old location is left intact.
    """
    if cmd.code == CmdCode.N:
        ship = replace(ship, north=ship.north + cmd.value)
    elif cmd.code == CmdCode.S:
        ship = replace(ship, north=ship.north - cmd.value)
    elif cmd.code == CmdCode.E:
        ship = replace(ship, east=ship.east + cmd.value)
    elif cmd.code == CmdCode.W:
        ship = replace(ship, east=ship.east - cmd.value)
    elif cmd.code == CmdCode.R:
        ship = replace(ship, angle=(ship.angle + cmd.value) % 360)
    elif cmd.code == CmdCode.L:
        ship = replace(ship, angle=(ship.angle - cmd.value) % 360)
    elif cmd.code == CmdCode.F:
        if ship.angle == 0:
            ship = move_ship(ship, Command(CmdCode.E, cmd.value))
        elif ship.angle == 90:
            ship = move_ship(ship, Command(CmdCode.S, cmd.value))
        elif ship.angle == 180:
            ship = move_ship(ship, Command(CmdCode.W, cmd.value))
        elif ship.angle == 270:
            ship = move_ship(ship, Command(CmdCode.N, cmd.value))
        else:
            raise ValueError(f"Invalid location angle: {ship.angle!r}")
    else:
        raise ValueError(f"Unexpected command code: {cmd!r}")

    return ship


@dataclass
class WaypointShip:
    # Ship coordinates
    ship_north: int = 0
    ship_east: int = 0

    # Waypoint coordinates relative to the ship
    wp_north: int = 1
    wp_east: int = 10


def move_waypoint_ship(ws: WaypointShip, cmd: Command) -> WaypointShip:
    """
    Calculates the new location for the ship and the waypoint
    after execution of the command.
    Returns the new WaypointShip object, the old object is left intact.
    """
    if cmd.code == CmdCode.N:
        ws = replace(ws, wp_north=ws.wp_north + cmd.value)
    elif cmd.code == CmdCode.S:
        ws = replace(ws, wp_north=ws.wp_north - cmd.value)
    elif cmd.code == CmdCode.E:
        ws = replace(ws, wp_east=ws.wp_east + cmd.value)
    elif cmd.code == CmdCode.W:
        ws = replace(ws, wp_east=ws.wp_east - cmd.value)
    elif cmd.code == CmdCode.R:
        if cmd.value == 90:
            ws = replace(ws, wp_north=-ws.wp_east, wp_east=ws.wp_north)
        elif cmd.value == 180:
            ws = replace(ws, wp_north=-ws.wp_north, wp_east=-ws.wp_east)
        elif cmd.value == 270:
            ws = replace(ws, wp_north=ws.wp_east, wp_east=-ws.wp_north)
        else:
            raise ValueError(f"Invalid command angle: {cmd.value!r}")
    elif cmd.code == CmdCode.L:
        if cmd.value in [90, 180, 270]:
            ws = move_waypoint_ship(ws, Command(CmdCode.R, 360 - cmd.value))
        else:
            raise ValueError(f"Invalid command angle: {cmd.value!r}")
    elif cmd.code == CmdCode.F:
        ws = replace(
            ws,
            ship_north=ws.ship_north + ws.wp_north * cmd.value,
            ship_east=ws.ship_east + ws.wp_east * cmd.value,
        )
    else:
        raise ValueError(f"Unexpected command code: {cmd!r}")

    return ws


def main():
    with open('./input.txt') as f:
        lines = f.readlines()
        commands = [parse_command(l) for l in lines]

    ship = Ship()
    for cmd in commands:
        ship = move_ship(ship, cmd)

    manhattan_distance = abs(ship.north) + abs(ship.east)
    print(f"Manhattan distance: {manhattan_distance}")

    ws = WaypointShip()
    for cmd in commands:
        ws = move_waypoint_ship(ws, cmd)

    manhattan_distance = abs(ws.ship_north) + abs(ws.ship_east)
    print(f"Manhattan distance with waypoint: {manhattan_distance}")


if __name__ == "__main__":
    main()
