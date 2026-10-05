"""Тесты класса Ingredient."""
from models import Ingredient


def test_ingredient_creation():
    ing = Ingredient(1, "Рис", "г")
    assert ing.id == 1
    assert ing.name == "рис"
    assert ing.unit == "г"


def test_ingredient_str():
    ing = Ingredient(1, "курица", "г")
    assert "курица" in str(ing)


def test_ingredient_from_data():
    data = {"id": 5, "name": "Овощи", "unit": "г"}
    ing = Ingredient.from_data(data)
    assert ing.id == 5
    assert ing.name == "овощи"


def test_ingredient_to_dict():
    ing = Ingredient(3, "соль", "г")
    assert ing.to_dict() == {"id": 3, "name": "соль", "unit": "г"}


def test_validate_name():
    assert Ingredient.validate_name("соль")
    assert not Ingredient.validate_name("   ")