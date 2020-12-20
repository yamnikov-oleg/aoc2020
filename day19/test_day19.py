import pytest

from day19 import CharRule, ComplexRule, is_valid, parse_rules

# 0: 1 2
# 1: "a"
# 2: 1 3 | 3 1
# 3: "b"
TEST_RULE_1 = ComplexRule([
    [CharRule("a"), ComplexRule([
        [CharRule("a"), CharRule("b")], [CharRule("b"), CharRule("a")],
    ])],
])

# 0: 4 1 5
# 1: 2 3 | 3 2
# 2: 4 4 | 5 5
# 3: 4 5 | 5 4
# 4: "a"
# 5: "b"
TEST_RULE_2 = ComplexRule([
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
])


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
    (TEST_RULE_1, {"aab", "aba"}),
    (TEST_RULE_2, {"aaaabb", "aaabab", "abbabb", "abbbab", "aabaab", "aabbbb", "abaaab", "ababbb"}),
])
def test_rule_iter_valid_values(rule, value_set):
    assert set(rule.iter_valid_values()) == value_set


@pytest.mark.parametrize("rule,value,result", [
    (TEST_RULE_1, "aab", True),
    (TEST_RULE_1, "abb", False),
    (TEST_RULE_1, "aaba", False),
    (TEST_RULE_1, "aa", False),
])
def test_is_valid(rule, value, result):
    assert is_valid(rule, value) == result
