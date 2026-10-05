"""Тесты модуля storage (JSON ↔ объекты)."""
import storage
from models import Dish, Ingredient


def test_save_and_load_dishes(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    dishes = [Dish(1, "Омлет", ["яйца"], 150, "завтрак")]
    storage.save_dishes(dishes, "dishes.json")
    loaded = storage.load_dishes("dishes.json")
    assert len(loaded) == 1
    assert loaded[0].name == "Омлет"
    assert loaded[0].meal.name == "завтрак"


def test_save_and_load_ingredients(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    ingredients = [Ingredient(1, "рис", "г")]
    storage.save_ingredients(ingredients, "ingredients.json")
    loaded = storage.load_ingredients("ingredients.json")
    assert loaded[0].name == "рис"


def test_load_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    assert storage.load_dishes("no_such.json") == []