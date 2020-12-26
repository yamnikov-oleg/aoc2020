import pytest

from day21 import (FoodItem, find_safe_ingredients, match_allergens,
                   parse_food_item)


@pytest.mark.parametrize("line, food_item", [
    ("sqjhc fvjkl (contains soy)", FoodItem(["sqjhc", "fvjkl"], ["soy"])),
    (
        "mxmxvkd kfcds sqjhc nhms (contains dairy, fish)",
        FoodItem(["mxmxvkd", "kfcds", "sqjhc", "nhms"], ["dairy", "fish"]),
    ),
])
def test_parse_food_item(line, food_item):
    assert parse_food_item(line) == food_item


def test_find_safe_ingredients():
    food_items = [
        parse_food_item("mxmxvkd kfcds sqjhc nhms (contains dairy, fish)"),
        parse_food_item("trh fvjkl sbzzf mxmxvkd (contains dairy)"),
        parse_food_item("sqjhc fvjkl (contains soy)"),
        parse_food_item("sqjhc mxmxvkd sbzzf (contains fish)"),
    ]
    safe_ingredients = {"kfcds", "nhms", "sbzzf", "trh"}
    assert find_safe_ingredients(food_items) == safe_ingredients


def test_match_allergens():
    food_items = [
        parse_food_item("mxmxvkd kfcds sqjhc nhms (contains dairy, fish)"),
        parse_food_item("trh fvjkl sbzzf mxmxvkd (contains dairy)"),
        parse_food_item("sqjhc fvjkl (contains soy)"),
        parse_food_item("sqjhc mxmxvkd sbzzf (contains fish)"),
    ]
    assert match_allergens(food_items) == {
        'dairy': 'mxmxvkd',
        'fish': 'sqjhc',
        'soy': 'fvjkl',
    }
