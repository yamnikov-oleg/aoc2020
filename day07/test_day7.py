from day7 import Rule, count_bags_inside, parse_rule, which_colors_can_contain


def test_parse_rule():
    cases = [
        (
            "light red bags contain 1 bright white bag, 2 muted yellow bags.",
            Rule(color='light red', contains=[(1, 'bright white'), (2, 'muted yellow')]),
        ),
        (
            "bright white bags contain 1 shiny gold bag.",
            Rule(color='bright white', contains=[(1, 'shiny gold')]),
        ),
        (
            "bright white bags contain 1 shiny gold bag.\n",  # with newline
            Rule(color='bright white', contains=[(1, 'shiny gold')]),
        ),
        (
            "faded blue bags contain no other bags.",
            Rule(color='faded blue', contains=[]),
        ),
    ]

    for line, rule in cases:
        assert parse_rule(line) == rule


def test_which_colors_can_contain():
    which_colors = which_colors_can_contain(
        rules=[
            Rule(color='light red', contains=[(1, 'bright white'), (2, 'muted yellow')]),
            Rule(color='dark orange', contains=[(3, 'bright white'), (4, 'muted yellow')]),
            Rule(color='bright white', contains=[(1, 'shiny gold')]),
            Rule(color='muted yellow', contains=[(2, 'shiny gold'), (9, 'faded blue')]),
            Rule(color='shiny gold', contains=[(1, 'dark olive'), (2, 'vibrant plum')]),
            Rule(color='dark olive', contains=[(3, 'faded blue'), (4, 'dotted black')]),
            Rule(color='vibrant plum', contains=[(5, 'faded blue'), (6, 'dotted black')]),
            Rule(color='faded blue', contains=[]),
            Rule(color='dotted black', contains=[]),
        ],
        target_color='shiny gold',
    )
    assert which_colors == {'bright white', 'dark orange', 'light red', 'muted yellow'}


def test_count_bags_inside():
    count = count_bags_inside(
        rules=[
            Rule(color='shiny gold', contains=[(2, 'dark red')]),
            Rule(color='dark red', contains=[(2, 'dark orange')]),
            Rule(color='dark orange', contains=[(2, 'dark yellow')]),
            Rule(color='dark yellow', contains=[(2, 'dark green')]),
            Rule(color='dark green', contains=[(2, 'dark blue')]),
            Rule(color='dark blue', contains=[(2, 'dark violet')]),
            Rule(color='dark violet', contains=[]),
        ],
        target_color='shiny gold',
    )
    assert count == 126
