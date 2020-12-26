import re
from dataclasses import dataclass
from typing import Dict, List, Set


@dataclass
class FoodItem:
    ingredients: List[str]
    allergens: List[str]


def parse_food_item(line: str) -> FoodItem:
    """
    Example::

        parse_food_item("mxmxvkd kfcds sqjhc nhms (contains dairy, fish)")
        # => FoodItem(ingredients=["mxmxvkd", "kfcds", "sqjhc", "nhms"], allergens=["dairy", "fish"])
    """
    regex = re.compile(r'^([\w ]+) \(contains ([\w \,]+)\)$')
    match = regex.match(line)
    if not match:
        raise ValueError(f"Invalid food item: {line!r}")

    ingredients = match.group(1).split(' ')
    allergens = match.group(2).split(', ')
    return FoodItem(ingredients, allergens)


def match_allergens_partially(food_items: List[FoodItem]) -> Dict[str, Set[str]]:
    """
    Finds possibly matching ingredients for each allergen.

    :returns: A dict which map each allergen's name to a set of ingredient names.
        The listed ingredients can possibly but not necessarily contain the allergen.
        Pass the returned dict to reduce_partial_matches to try to find exact matches.
    """
    possible_matches: Dict[str, Set[str]] = {}
    for item in food_items:
        for allergen in item.allergens:
            possible_allergen_ingredients = set(item.ingredients)
            if allergen in possible_matches:
                possible_matches[allergen] &= possible_allergen_ingredients
            else:
                possible_matches[allergen] = possible_allergen_ingredients

    return possible_matches


def reduce_partial_matches(partial_matches: Dict[str, Set[str]]) -> Dict[str, str]:
    """
    Given a dict returned by match_allergens_partially, tries to find one matching
    ingredient for each allergen.

    :returns: A dict which maps an allergen's name to an ingredient's name.

    :raises ValueError: if the allergens cannot be matched exactly.
    """
    if not partial_matches:
        return {}

    exact_match_allergen = None
    exact_match_ingredient = None
    for allergen, ingredients in partial_matches.items():
        if len(ingredients) == 0:
            raise ValueError(f"Allergen {allergen!r} can't be matched to any ingredient")
        elif len(ingredients) == 1:
            exact_match_allergen = allergen
            exact_match_ingredient = next(iter(ingredients))
            break
        else:
            continue

    if not exact_match_allergen:
        raise ValueError("Allergens cannot be matched")

    rest_of_matches = {}
    for allergen, ingredients in partial_matches.items():
        if allergen == exact_match_allergen:
            continue

        rest_of_ingredients = ingredients - {exact_match_ingredient}

        rest_of_matches[allergen] = rest_of_ingredients

    submatches = reduce_partial_matches(rest_of_matches)
    return {**submatches, exact_match_allergen: exact_match_ingredient}


def match_allergens(food_items: List[FoodItem]) -> Dict[str, str]:
    """
    Tries to find one matching ingredient for each allergen.

    :returns: A dict which maps an allergen's name to an ingredient's name.

    :raises ValueError: if the allergens cannot be matched exactly.
    """
    partial_matches = match_allergens_partially(food_items)
    return reduce_partial_matches(partial_matches)


def find_safe_ingredients(food_items: List[FoodItem]) -> Set[str]:
    """
    Finds ingredients which cannot possible contain any of the listed allergens.

    :returns: A set of found ingredients.
    """
    all_ingredients = set()
    for item in food_items:
        all_ingredients.update(item.ingredients)

    allergens_map = match_allergens_partially(food_items)

    unsafe_ingredients = set()
    for allergen, ingredients in allergens_map.items():
        unsafe_ingredients.update(ingredients)

    safe_ingredients = all_ingredients - unsafe_ingredients

    return safe_ingredients


def get_canonical_dangerous_string(allergen_map: Dict[str, str]) -> str:
    """
    Given a map of allergens to ingredients, constructs a "canonical dangerous ingredient list".
    """
    sorted_pairs = sorted(allergen_map.items(), key=lambda pair: pair[0])
    return ','.join([ingredient for allergen, ingredient in sorted_pairs])


def main():
    with open('./input.txt') as f:
        food_items = [parse_food_item(line.strip()) for line in f.readlines()]

    safe_ingredients = find_safe_ingredients(food_items)

    safe_occurences = 0
    for ingredient in safe_ingredients:
        for item in food_items:
            if ingredient in item.ingredients:
                safe_occurences += 1

    print(f"Safe ingredients: {safe_ingredients}")
    print(f"They occur {safe_occurences} times")

    allergen_map = match_allergens(food_items)
    dangerous_string = get_canonical_dangerous_string(allergen_map)
    print(f"Allergen map: {allergen_map}")
    print(f"Canonical dangerous string: {dangerous_string}")


if __name__ == "__main__":
    main()
