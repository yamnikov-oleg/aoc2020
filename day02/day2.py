import re
from dataclasses import dataclass


@dataclass
class PasswordEntry:
    first_pos: int
    second_pos: int
    symbol: str
    password: str


def parse_input_line(line: str) -> PasswordEntry:
    """
    Raises ValueError if the line cannot be parsed.
    """
    regex = re.compile(r'(\d+)-(\d+) (\w): (\w+)')
    match = regex.match(line)
    if not match:
        raise ValueError(f"Line {line:!r} has an invalid format!")

    return PasswordEntry(
        first_pos=int(match.group(1)),
        second_pos=int(match.group(2)),
        symbol=match.group(3),
        password=match.group(4),
    )


def is_valid_count_policy(entry: PasswordEntry) -> bool:
    symbol_count = entry.password.count(entry.symbol)
    return entry.first_pos <= symbol_count <= entry.second_pos


def is_valid_position_policy(entry: PasswordEntry) -> bool:
    first_matches = entry.password[entry.first_pos - 1] == entry.symbol
    second_matches = entry.password[entry.second_pos - 1] == entry.symbol
    if first_matches and not second_matches:
        return True
    elif not first_matches and second_matches:
        return True
    else:
        return False


def main():
    with open('./input.txt') as f:
        lines = f.readlines()
        entries = [parse_input_line(l) for l in lines]

    count_valid_count_policy = 0
    count_valid_position_policy = 0
    for entry in entries:
        if is_valid_count_policy(entry):
            count_valid_count_policy += 1
        if is_valid_position_policy(entry):
            count_valid_position_policy += 1

    print(f"Valid by the first policy: {count_valid_count_policy}")
    print(f"Valid by the second policy: {count_valid_position_policy}")


if __name__ == "__main__":
    main()
