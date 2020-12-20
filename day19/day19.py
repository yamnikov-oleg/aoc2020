import re
from dataclasses import dataclass
from typing import Dict, List


class Rule:
    """
    The base class for other string validation rules.
    Provides single interface for them.
    """
    def consume(self, line: str) -> List[str]:
        """
        Parses substrings, which are valid by this rule, from the start of the line.

        :returns: the list of all possible remainders left after parsing all
        possible substrings.

        Some examples:

        * If the line is invalid, returns an empty list (there is no valid substring)::

            rule.consume("aba")  # => []
            # "aba" is invalid

        * If there is only one matching substring, returns a list of the single remainder::

            rule.consume("aba")  # => ["a"]
            # "ab" matches the rule, "a" is the remainder

        * If there are multiple matches, returns multiple remainders::

            rule.consume("aba")  # => ["a", "ba"]
            # "a" and "ab" both match the rule

        * If the input line matches the rule entirely, the output list will contain
          an empty string, which means that the line was consumes entirely::

            rule.consume("aba")  # => ["a", ""]
            # "ab" and "aba" both match
        """
        raise NotImplementedError("consume")


@dataclass
class CharRule(Rule):
    """
    A rule which matches a single character.
    """
    char: str

    def consume(self, line: str) -> List[str]:
        if not line:
            return []

        if line[0] != self.char:
            return []

        return [line[1:]]


@dataclass
class ComplexRule(Rule):
    """
    A rule which matches one of the sequences of rules (the subrules).
    """
    # Each item in the list is a subrule.
    # A subrule is a sequence of rules that matches a single string.
    subrules: List[List[Rule]]

    def consume(self, line: str) -> List[str]:
        remainders = []
        for subrule in self.subrules:
            remainders.extend(consume_seq(subrule, line))

        return remainders


def consume_seq(rules: List[Rule], line: str) -> List[str]:
    """
    Consumes the line by the each rule in the sequence one by one.
    Returns all remainders after consuming all valid substrings.

    Example:

    Given that rule1 matches "a" and rule2 matches "b" or "bb", calling::

        consume_seq([rule1, rule2], "abba")

    would return (possible in different order)::

        ["a", "ba"]

    because "abb" and "ab" match the sequence of rule1 and rule2.
    """
    if not rules:
        return []

    if len(rules) == 1:
        return rules[0].consume(line)

    seq_remainders = []
    for remainder in rules[0].consume(line):
        seq_remainders.extend(consume_seq(rules[1:], remainder))

    return seq_remainders


def split_rule_texts(content: str) -> Dict[int, str]:
    """
    Split the rules file into a dictionary, which matches the number of each rule
    to the text of said rule.

    Example::

        split_rule_texts('0: "a"\n1: 0 0')
        # => {0: '"a"', 1: '0 0'}
    """
    generic_rule_re = re.compile(r'^(\d+): (.+)$')
    rule_texts: Dict[int, str] = {}
    for line in content.splitlines():
        match = generic_rule_re.match(line)
        if not match:
            raise ValueError(f"Invalid rule: {line}")

        rule_number = int(match.group(1))
        rule_text = match.group(2)
        rule_texts[rule_number] = rule_text

    return rule_texts


def parse_complex_rule_text(text: str) -> List[List[int]]:
    """
    Parses the text of a complex rule into a list of lists of number.

    Example::

        parse_complex_rule_text('1 2 | 3 4')
        # => [[1, 2], [3, 4]]
    """
    subrule_numbers = []
    subrule_texts = text.split('|')
    for subrule_text in subrule_texts:
        subrule = []
        for ref_number_str in subrule_text.strip().split(' '):
            ref_number = int(ref_number_str)
            subrule.append(ref_number)
        subrule_numbers.append(subrule)

    return subrule_numbers


def parse_rule_texts(rule_texts: Dict[int, str]) -> Dict[int, Rule]:
    """
    Parses rule texts.

    :param rule_texts: a dictionary of rule texts, as returned by split_rule_texts.
    :returns: a dictionary which maps a rule's number to the rule.
    """
    rules: Dict[int, Rule] = {}

    char_rule_re = re.compile(r'^"(.+)"$')
    complex_rule_re = re.compile(r'^[\d\s\|]+$')

    def parse_rule_text(number: int) -> Rule:
        if number in rules:
            return rules[number]

        if match := char_rule_re.match(rule_texts[number]):
            rule = CharRule(match.group(1))
        elif match := complex_rule_re.match(rule_texts[number]):
            rule = ComplexRule([])
            subrule_numbers = parse_complex_rule_text(rule_texts[number])
            for subrule_numbers_item in subrule_numbers:
                subrule = []
                for ref_number in subrule_numbers_item:
                    if ref_number == number:
                        subrule.append(rule)
                    else:
                        subrule.append(parse_rule_text(ref_number))
                rule.subrules.append(subrule)
        else:
            raise ValueError(f"Invalud rule: {rule_texts[number]}")

        rules[number] = rule
        return rule

    parse_rule_text(0)

    for rule_number in rule_texts.keys():
        if rule_number not in rules:
            raise ValueError(f"Rule {rule_number} is not referenced from rule 0")

    return rules


def is_valid(rule: Rule, line: str) -> bool:
    """
    Validates the line against the rule.

    :returns: True if the line matches the rule.
    """
    remainders = rule.consume(line)
    return "" in remainders


def main():
    with open('./input.txt') as f:
        content = f.read()
        rules_content, values_content = content.split('\n\n')

    rule_texts = split_rule_texts(rules_content)
    rules = parse_rule_texts(rule_texts)
    values = values_content.splitlines()

    valid_values = []
    for value in values:
        if is_valid(rules[0], value):
            valid_values.append(value)

    print(f"Valid values: {len(valid_values)}")

    rec_rule_texts = rule_texts.copy()
    rec_rule_texts[8] = '42 | 42 8'
    rec_rule_texts[11] = '42 31 | 42 11 31'
    rec_rules = parse_rule_texts(rec_rule_texts)

    valid_values = []
    for value in values:
        if is_valid(rec_rules[0], value):
            valid_values.append(value)

    print(f"Valid values: {len(valid_values)}")


if __name__ == "__main__":
    main()
