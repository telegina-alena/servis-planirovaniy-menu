
"""Импорт данных из JSON-файлов в SQLite."""

import json
from pathlib import Path

from db.database import get_connection
from models.meals import Meal


BASE_DIR = Path(__file__).resolve().parent.parent

DISHES_FILE = BASE_DIR / "data" / "dishes.json"
INGREDIENTS_FILE = BASE_DIR / "data" / "ingredients.json"


def load_json(filename: Path) -> list[dict]:
    """Загрузить данные из JSON-файла."""

    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_meals(conn) -> dict[str, int]:
    """Импортировать приёмы пищи и вернуть их идентификаторы."""

    conn.executemany(
        "INSERT INTO meals (name) VALUES (?)",
        [(name,) for name in Meal.available_meals()],
    )

    rows = conn.execute(
        "SELECT id, name FROM meals"
    ).fetchall()

    return {name: meal_id for meal_id, name in rows}


def import_ingredients(conn) -> dict[str, int]:
    """Импортировать ингредиенты и вернуть их идентификаторы."""

    ingredients = load_json(INGREDIENTS_FILE)

    conn.executemany(
        """
        INSERT INTO ingredients (id, name, unit)
        VALUES (?, ?, ?)
        """,
        [
            (
                item["id"],
                item["name"],
                item.get("unit", "шт"),
            )
            for item in ingredients
        ],
    )

    return {
        item["name"]: item["id"]
        for item in ingredients
    }


def import_dishes(
    conn,
    meal_ids: dict[str, int],
    ingredient_ids: dict[str, int],
) -> None:
    """Импортировать блюда и связи с ингредиентами."""

    dishes = load_json(DISHES_FILE)

    conn.executemany(
        """
        INSERT INTO dishes (id, name, calories, meal_id)
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                dish["id"],
                dish["name"],
                dish["calories"],
                meal_ids[dish["meal"]],
            )
            for dish in dishes
        ],
    )

    relations = []

    for dish in dishes:
        for ingredient_name in dish["ingredients"]:
            if ingredient_name not in ingredient_ids:
                raise ValueError(
                    f"Ингредиент не найден: {ingredient_name}"
                )

            relations.append(
                (
                    dish["id"],
                    ingredient_ids[ingredient_name],
                )
            )

    conn.executemany(
        """
        INSERT INTO dish_ingredients (dish_id, ingredient_id)
        VALUES (?, ?)
        """,
        relations,
    )


def main() -> None:
    """Выполнить полный импорт данных из JSON."""

    conn = get_connection()

    try:
        # Очищаем старые данные перед повторным импортом.
        conn.execute("DELETE FROM dish_ingredients")
        conn.execute("DELETE FROM dishes")
        conn.execute("DELETE FROM ingredients")
        conn.execute("DELETE FROM meals")

        meal_ids = import_meals(conn)
        ingredient_ids = import_ingredients(conn)

        import_dishes(
            conn,
            meal_ids,
            ingredient_ids,
        )

        conn.commit()

        print("Импорт данных успешно завершён!")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()
