
"""Сохранение и загрузка данных с преобразованием в объекты."""

import json
from pathlib import Path

from models import Dish, Ingredient


DATA_DIR = Path(__file__).parent / "data"


def _read_raw(filename: str) -> list[dict]:
    """Прочитать JSON-файл и вернуть список словарей."""

    path = DATA_DIR / filename

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            print(f"Файл {filename} содержит некорректные данные.")
            return []

        if not all(isinstance(item, dict) for item in data):
            print(f"Файл {filename} содержит некорректные записи.")
            return []

        return data

    except FileNotFoundError:
        print(f"Файл {filename} не найден, создан пустой список.")
        return []

    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, создан пустой список.")
        return []


def _write_raw(filename: str, data: list[dict]) -> None:
    """Записать список словарей в JSON-файл."""

    path = DATA_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# ---------- Блюда ----------

def load_dishes(filename: str = "dishes.json") -> list[Dish]:
    """Загрузить блюда из JSON в виде объектов Dish."""

    return [Dish.from_data(d) for d in _read_raw(filename)]


def save_dishes(
    dishes: list[Dish], filename: str = "dishes.json"
) -> None:
    """Сохранить объекты Dish в JSON."""

    _write_raw(filename, [d.to_dict() for d in dishes])


# ---------- Ингредиенты ----------

def load_ingredients(
    filename: str = "ingredients.json"
) -> list[Ingredient]:
    """Загрузить ингредиенты из JSON в виде объектов Ingredient."""

    return [Ingredient.from_data(d) for d in _read_raw(filename)]


def save_ingredients(
    ingredients: list[Ingredient], filename: str = "ingredients.json"
) -> None:
    """Сохранить объекты Ingredient в JSON."""

    _write_raw(filename, [i.to_dict() for i in ingredients])


def ingredient_names(ingredients: list[Ingredient]) -> list[str]:
    """Вернуть список имён ингредиентов для проверки доступности."""

    return [i.name for i in ingredients]