from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple


@dataclass
class Field:
    name: str
    ranges: List[Tuple[int, int]] = field(default_factory=list)

    def is_valid(self, value: int) -> bool:
        for range_from, range_to in self.ranges:
            if range_from <= value <= range_to:
                return True

        return False


def parse_field(line: str) -> Field:
    line = line.strip()

    try:
        name, raw_ranges = line.split(": ")
        raw_ranges = raw_ranges.split(" or ")
        ranges = []
        for raw_range in raw_ranges:
            lower, upper = raw_range.split('-')
            ranges.append((int(lower), int(upper)))
    except ValueError:
        raise ValueError(f"Invalid field: {line!r}")

    return Field(name, ranges)


@dataclass
class Ticket:
    # THE NUMBERS MASON!
    numbers: List[int]


def parse_ticket(line: str) -> Ticket:
    return Ticket([int(n) for n in line.strip().split(',')])


def parse_notes(notes: str) -> Tuple[List[Field], Ticket, List[Ticket]]:
    """
    Parses the notes (the puzzle input) and returns the field, your ticket
    and nearby tickets in order.
    """
    sections = notes.strip().split('\n\n')

    fields_lines = sections[0].split('\n')
    fields = [parse_field(line) for line in fields_lines]

    your_ticket_lines = sections[1].split('\n')
    your_ticket = parse_ticket(your_ticket_lines[1])

    nearby_tickets_lines = sections[2].split('\n')
    nearby_tickets = [parse_ticket(line) for line in nearby_tickets_lines[1:]]

    return fields, your_ticket, nearby_tickets


def find_invalid_values(fields: List[Field], tickets: List[Ticket]) -> List[int]:
    """
    Returns the list of values from the tickets that are invalid for all of the fields.
    """
    invalid_values = []
    for ticket in tickets:
        for value in ticket.numbers:
            is_invalid = all(not field.is_valid(value) for field in fields)
            if is_invalid:
                invalid_values.append(value)

    return invalid_values


def ticket_is_valid(fields: List[Field], ticket: Ticket) -> bool:
    for value in ticket.numbers:
        is_invalid = all(not field.is_valid(value) for field in fields)
        if is_invalid:
            return False

    return True


def find_matching_fields(fields: List[Field], tickets: List[Ticket]) -> Dict[int, Set[str]]:
    """
    For each value index in the tickets finds fields which match it. A field matches
    a value index if all values at said index in all tickets are valid for this field.

    Returns a dict with value indices as keys and sets of field names as value.
    """
    index_fields: Dict[int, Set[str]] = {}

    for ticket in tickets:
        for value_index, value in enumerate(ticket.numbers):
            matching_fields = set(field.name for field in fields if field.is_valid(value))
            if value_index in index_fields:
                index_fields[value_index] &= matching_fields
            else:
                index_fields[value_index] = matching_fields

    return index_fields


def resolve_matching_fields(field_matches: Dict[int, Set[str]]) -> Dict[int, str]:
    """
    Given a dict that matches each index to a set of matching fields, tries to find
    a valid selection of one field for each index. Raises ValueError if there are
    multiple solutions.

    Returns a mapping from each index to the selected field name.
    """
    if len(field_matches) == 0:
        return {}

    # Find an index for which there is already one matching field.
    solved_index = None
    solved_field = None
    for index, fields in field_matches.items():
        if len(fields) == 1:
            solved_index = index
            solved_field, = fields  # Unpack the only value from the set
            break

    if solved_index is None:
        raise ValueError(f"Multiple solutions for field matches: {field_matches}")

    # Make a copy of field_matches without solved_index and solved_field
    reduced_field_matches = {index: fields.copy() for index, fields in field_matches.items()}
    del reduced_field_matches[solved_index]
    for index, fields in reduced_field_matches.items():
        if solved_field in fields:
            fields.remove(solved_field)

    resolved_matches = resolve_matching_fields(reduced_field_matches)
    resolved_matches[solved_index] = solved_field

    return resolved_matches


def determine_field_order(fields: List[Field], tickets: List[Ticket]) -> List[Field]:
    """
    Returns the fields in the order they appear in the tickets.
    """
    # Filter out invalid tickets
    tickets = [t for t in tickets if ticket_is_valid(fields, t)]

    # Map each index to the matching field name
    index_fields = resolve_matching_fields(find_matching_fields(fields, tickets))

    # Sort matches by index
    sorted_index_fields = sorted(index_fields.items(), key=lambda pair: pair[0])

    ordered_fields = []
    for index, name in sorted_index_fields:
        for f in fields:
            if f.name == name:
                ordered_fields.append(f)

    return ordered_fields


def main():
    with open('./input.txt') as f:
        fields, your_ticket, nearby_tickets = parse_notes(f.read())

    invalid_values = find_invalid_values(fields, nearby_tickets)
    print(f"Sum of invalid values: {sum(invalid_values)}")

    ordered_fields = determine_field_order(fields, nearby_tickets)
    answer_mult = 1
    for index, f in enumerate(ordered_fields):
        if f.name.startswith("departure"):
            answer_mult *= your_ticket.numbers[index]
    print(f"Multiplication of the departure field values: {answer_mult}")


if __name__ == "__main__":
    main()
