from day6 import (GroupAnswers, PersonAnswers,
                  get_sum_of_anyone_answered_yes_to,
                  get_sum_of_everyone_answered_yes_to, parse_answers)


def test_parse_answers():
    cases = [
        (
            (
                "abcx\n"
                "abcy\n"
                "abcz\n"
            ),
            [
                GroupAnswers(people_answers=[
                    PersonAnswers(answered_yes_to=["a", "b", "c", "x"]),
                    PersonAnswers(answered_yes_to=["a", "b", "c", "y"]),
                    PersonAnswers(answered_yes_to=["a", "b", "c", "z"]),
                ]),
            ],
        ),

        (
            (
                "abc\n"
                "\n"
                "a\n"
                "b\n"
                "c\n"
                "\n"
                "ab\n"
                "ac\n"
                "\n"
                "a\n"
                "a\n"
                "a\n"
                "a\n"
                "\n"
                "b"
            ),
            [
                GroupAnswers(people_answers=[
                    PersonAnswers(answered_yes_to=["a", "b", "c"]),
                ]),
                GroupAnswers(people_answers=[
                    PersonAnswers(answered_yes_to=["a"]),
                    PersonAnswers(answered_yes_to=["b"]),
                    PersonAnswers(answered_yes_to=["c"]),
                ]),
                GroupAnswers(people_answers=[
                    PersonAnswers(answered_yes_to=["a", "b"]),
                    PersonAnswers(answered_yes_to=["a", "c"]),
                ]),
                GroupAnswers(people_answers=[
                    PersonAnswers(answered_yes_to=["a"]),
                    PersonAnswers(answered_yes_to=["a"]),
                    PersonAnswers(answered_yes_to=["a"]),
                    PersonAnswers(answered_yes_to=["a"]),
                ]),
                GroupAnswers(people_answers=[
                    PersonAnswers(answered_yes_to=["b"]),
                ]),
            ],
        )
    ]

    for input, output in cases:
        assert parse_answers(input) == output


def test_get_sum_of_anyone_answered_yes_to():
    cases = [
        (
            [
                GroupAnswers(people_answers=[
                    PersonAnswers(answered_yes_to=["a", "b", "c"]),
                ]),
                GroupAnswers(people_answers=[
                    PersonAnswers(answered_yes_to=["a"]),
                    PersonAnswers(answered_yes_to=["b"]),
                    PersonAnswers(answered_yes_to=["c"]),
                ]),
                GroupAnswers(people_answers=[
                    PersonAnswers(answered_yes_to=["a", "b"]),
                    PersonAnswers(answered_yes_to=["a", "c"]),
                ]),
                GroupAnswers(people_answers=[
                    PersonAnswers(answered_yes_to=["a"]),
                    PersonAnswers(answered_yes_to=["a"]),
                    PersonAnswers(answered_yes_to=["a"]),
                    PersonAnswers(answered_yes_to=["a"]),
                ]),
                GroupAnswers(people_answers=[
                    PersonAnswers(answered_yes_to=["b"]),
                ]),
            ],
            11,
        )
    ]

    for input, output in cases:
        assert get_sum_of_anyone_answered_yes_to(input) == output


def test_get_sum_of_everyone_answered_yes_to():
    cases = [
        (
            [
                GroupAnswers(people_answers=[
                    PersonAnswers(answered_yes_to=["a", "b", "c"]),
                ]),
                GroupAnswers(people_answers=[
                    PersonAnswers(answered_yes_to=["a"]),
                    PersonAnswers(answered_yes_to=["b"]),
                    PersonAnswers(answered_yes_to=["c"]),
                ]),
                GroupAnswers(people_answers=[
                    PersonAnswers(answered_yes_to=["a", "b"]),
                    PersonAnswers(answered_yes_to=["a", "c"]),
                ]),
                GroupAnswers(people_answers=[
                    PersonAnswers(answered_yes_to=["a"]),
                    PersonAnswers(answered_yes_to=["a"]),
                    PersonAnswers(answered_yes_to=["a"]),
                    PersonAnswers(answered_yes_to=["a"]),
                ]),
                GroupAnswers(people_answers=[
                    PersonAnswers(answered_yes_to=["b"]),
                ]),
            ],
            6,
        )
    ]

    for input, output in cases:
        assert get_sum_of_everyone_answered_yes_to(input) == output
