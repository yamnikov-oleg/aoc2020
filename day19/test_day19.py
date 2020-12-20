import pytest

from day19 import CharRule, ComplexRule, parse_rules


@pytest.mark.parametrize("content,rules", [
    (
        (
            '0: 1 2\n'
            '1: "a"\n'
            '2: 1 3 | 3 1\n'
            '3: "b"\n'
        ),
        {
            0: ComplexRule([
                [CharRule("a"), ComplexRule([
                    [CharRule("a"), CharRule("b")], [CharRule("b"), CharRule("a")],
                ])],
            ]),
            1: CharRule("a"),
            2: ComplexRule([[CharRule("a"), CharRule("b")], [CharRule("b"), CharRule("a")]]),
            3: CharRule("b"),
        }
    ),
])
def test_parse_rules(content, rules):
    assert parse_rules(content) == rules


@pytest.mark.parametrize("rule,value_set", [
    (
        ComplexRule([
            [CharRule("a"), ComplexRule([
                [CharRule("a"), CharRule("b")], [CharRule("b"), CharRule("a")],
            ])],
        ]),
        {"aab", "aba"},
    ),
    (
        ComplexRule([
            [CharRule('a'), ComplexRule([
                [
                    ComplexRule([
                        [CharRule('a'), CharRule('a')],
                        [CharRule('b'), CharRule('b')],
                    ]), ComplexRule([
                        [CharRule('a'), CharRule('b')],
                        [CharRule('b'), CharRule('a')],
                    ])
                ], [
                    ComplexRule([
                        [CharRule('a'), CharRule('b')],
                        [CharRule('b'), CharRule('a')],
                    ]),
                    ComplexRule([
                        [CharRule('a'), CharRule('a')],
                        [CharRule('b'), CharRule('b')],
                    ])
                ]
            ]), CharRule('b')],
        ]),
        {"aaaabb", "aaabab", "abbabb", "abbbab", "aabaab", "aabbbb", "abaaab", "ababbb"},
    ),
])
def test_rule_iter_valid_values(rule, value_set):
    assert set(rule.iter_valid_values()) == value_set
