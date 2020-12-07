import re
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import List, Set, Tuple


@dataclass
class Rule:
    color: str
    # A list of [number, color] of bags the bag must contain
    contains: List[Tuple[int, str]] = field(default_factory=list)

    def can_contain(self, target_color: str) -> bool:
        """
        Returns True if target_colors is listed in self.contains.
        """
        for quantity, color in self.contains:
            if color == target_color:
                return True

        return False


def parse_rule(line: str) -> Rule:
    """
    Parses a line from input into a Rule object.
    Example:

    parse_rule("light red bags contain 1 bright white bag, 2 muted yellow bags.")
    # Returns:
    # Rule(color='light red', contains=[(1, 'bright white'), (2, 'muted yellow')])
    """
    # Remove extra white space
    line = line.strip()

    # Remove the period at the end
    if line.endswith('.'):
        line = line[:-1]

    # Extract the color and the part after "contain"
    match = re.match(r'^([\w ]+) bags contain ([\w\d, ]+)$', line)
    if not match:
        raise ValueError(f"Invalid rule: {line!r}")

    rule_color = match.group(1)
    contents = match.group(2)

    if contents == 'no other bags':
        return Rule(color=rule_color, contains=[])

    # Parse each rule after "contain"
    contents_split = contents.split(',')
    contains = []
    for content_rule in contents_split:
        content_rule = content_rule.strip()
        match = re.match(r'^(\d+) ([\w ]+) bags?$', content_rule)
        if not match:
            raise ValueError(f"Invalid content rule: {content_rule:!r}")

        contains_quantity = int(match.group(1))
        contains_color = match.group(2)
        contains.append((contains_quantity, contains_color))

    return Rule(color=rule_color, contains=contains)


def which_colors_can_contain(
            rules: List[Rule],
            target_color: str,
        ) -> Set[str]:
    """
    Returns a list of colors that can eventually contain the target color according
    to the rules.
    Assumes there are no loops in the rules.

    :param rules: the list of containment rules.
    :param target_color: the colors to be contained.
    """
    # Build a dict which maps each color to the list of colors which contain it.
    containment_map = {}
    for rule in rules:
        for quantity, contained_color in rule.contains:
            containment_map.setdefault(contained_color, [])
            containment_map[contained_color].append(rule.color)

    # Inner recursive function which traverses the containment_map
    def _which_colors_can_contain(target_color: str) -> Set[str]:
        can_contain = set()
        for color in containment_map.get(target_color, []):
            can_contain.add(color)
            can_contain.update(_which_colors_can_contain(color))
        return can_contain

    return _which_colors_can_contain(target_color)


def count_bags_inside(rules: List[Rule], target_color: str) -> int:
    """
    Returns how many bags must be contained inside a bag of target_color, recursively.
    Assumes there are no loops in the rules.
    Assumes there is only one rule for each color.
    """
    count = 0
    for rule in rules:
        if rule.color == target_color:
            for quantity, contained_color in rule.contains:
                count += quantity
                count += quantity * count_bags_inside(rules, contained_color)

            # Assumes there is only one rule for each color
            break

    return count


@contextmanager
def timeit():
    time_start = time.time()
    yield
    elapsed = time.time() - time_start
    print(f"[took {elapsed * 1000:0.2f}ms]")


def main():
    with open('./input.txt') as f:
        lines = f.readlines()
        rules = [parse_rule(l) for l in lines]

    with timeit():
        can_contain = which_colors_can_contain(rules, 'shiny gold')
        print(f"{len(can_contain)} colors can contain shiny gold")

    with timeit():
        inside_count = count_bags_inside(rules, 'shiny gold')
        print(f"Shiny gold contains {inside_count} bags inside")


if __name__ == "__main__":
    main()
