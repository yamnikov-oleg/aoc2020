import re
from dataclasses import dataclass
from typing import Dict, Iterator, List


class Rule:
    def iter_valid_values(self) -> Iterator[str]:
        raise NotImplementedError("iter_valid_values")


@dataclass
class CharRule(Rule):
    char: str

    def iter_valid_values(self) -> Iterator[str]:
        yield self.char


@dataclass
class ComplexRule(Rule):
    subrules: List[List[Rule]]

    def iter_valid_values(self) -> Iterator[str]:
        def concat_rules(rules):
            if len(rules) == 0:
                yield ""
                return

            for subvalue in concat_rules(rules[1:]):
                for value in rules[0].iter_valid_values():
                    yield value + subvalue

        for subrule in self.subrules:
            yield from concat_rules(subrule)


def parse_rules(content: str) -> Dict[int, Rule]:
    generic_rule_re = re.compile(r'^(\d+): (.+)$')
    rule_texts: Dict[int, str] = {}
    for line in content.splitlines():
        match = generic_rule_re.match(line)
        if not match:
            raise ValueError(f"Invalid rule: {line}")

        rule_number = int(match.group(1))
        rule_text = match.group(2)
        rule_texts[rule_number] = rule_text

    parsed_rules: Dict[int, Rule] = {}
    char_rule_re = re.compile(r'^"(.+)"$')
    complex_rule_re = re.compile(r'^[\d\s\|]+$')

    def parse_rule_text(number: int) -> Rule:
        if number in parsed_rules:
            return parsed_rules[number]

        if match := char_rule_re.match(rule_texts[number]):
            rule = CharRule(match.group(1))
        elif match := complex_rule_re.match(rule_texts[number]):
            subrule_texts = rule_texts[number].split('|')
            subrules = []
            for subrule_text in subrule_texts:
                subrule = []
                for ref_number_str in subrule_text.strip().split(' '):
                    ref_number = int(ref_number_str)
                    subrule.append(parse_rule_text(ref_number))
                subrules.append(subrule)
            rule = ComplexRule(subrules)
        else:
            raise ValueError(f"Invalud rule: {rule_texts[number]}")

        parsed_rules[number] = rule
        return rule

    parse_rule_text(0)

    for rule_number in rule_texts.keys():
        if rule_number not in parsed_rules:
            raise ValueError(f"Rule {rule_number} is not referenced from rule 0")

    return parsed_rules


def main():
    with open('./input.txt') as f:
        content = f.read()
        rules_content, values_content = content.split('\n\n')
        rules = parse_rules(rules_content)
        values = values_content.splitlines()

    valid_values = []
    for valid_value in rules[0].iter_valid_values():
        if valid_value in values:
            valid_values.append(valid_value)

    print(f"Valid values: {len(valid_values)}")


if __name__ == "__main__":
    main()
