import pytest

from day16 import (Field, Ticket, determine_field_order, find_invalid_values,
                   parse_field, parse_notes, parse_ticket)


@pytest.mark.parametrize("line,field", [
    ("class: 1-3 or 5-7", Field(name="class", ranges=[(1, 3), (5, 7)])),
    ("departure location: 40-261 or 279-955", Field(name="departure location", ranges=[(40, 261), (279, 955)])),
])
def test_parse_field(line, field):
    assert parse_field(line) == field


@pytest.mark.parametrize("line,ticket", [
    ("7,1,14", Ticket([7, 1, 14])),
])
def test_parse_ticket(line, ticket):
    assert parse_ticket(line) == ticket


@pytest.mark.parametrize("content,fields,your_ticket,nearby_tickets", [
    (
        (
            "class: 1-3 or 5-7\n"
            "row: 6-11 or 33-44\n"
            "seat: 13-40 or 45-50\n"
            "\n"
            "your ticket:\n"
            "7,1,14\n"
            "\n"
            "nearby tickets:\n"
            "7,3,47\n"
            "40,4,50\n"
            "55,2,20\n"
            "38,6,12\n"
        ),
        [
            Field(name="class", ranges=[(1, 3), (5, 7)]),
            Field(name="row", ranges=[(6, 11), (33, 44)]),
            Field(name="seat", ranges=[(13, 40), (45, 50)]),
        ],
        Ticket([7, 1, 14]),
        [
            Ticket([7, 3, 47]),
            Ticket([40, 4, 50]),
            Ticket([55, 2, 20]),
            Ticket([38, 6, 12]),
        ],
    ),
])
def test_parse_notes(content, fields, your_ticket, nearby_tickets):
    parsed = parse_notes(content)
    assert parsed[0] == fields
    assert parsed[1] == your_ticket
    assert parsed[2] == nearby_tickets


def test_find_invalid_values():
    fields = [
        Field(name="class", ranges=[(1, 3), (5, 7)]),
        Field(name="row", ranges=[(6, 11), (33, 44)]),
        Field(name="seat", ranges=[(13, 40), (45, 50)]),
    ]
    tickets = [
        Ticket([7, 3, 47]),
        Ticket([40, 4, 50]),
        Ticket([55, 2, 20]),
        Ticket([38, 6, 12]),
    ]
    assert find_invalid_values(fields, tickets) == [4, 55, 12]


def test_determine_field_order():
    fields = [
        Field(name="class", ranges=[(0, 1), (4, 19)]),
        Field(name="row", ranges=[(0, 5), (8, 19)]),
        Field(name="seat", ranges=[(0, 13), (16, 19)]),
    ]
    tickets = [
        Ticket([3, 9, 18]),
        Ticket([15, 1, 5]),
        Ticket([5, 14, 9]),
    ]
    assert determine_field_order(fields, tickets) == [
        Field(name="row", ranges=[(0, 5), (8, 19)]),
        Field(name="class", ranges=[(0, 1), (4, 19)]),
        Field(name="seat", ranges=[(0, 13), (16, 19)]),
    ]
