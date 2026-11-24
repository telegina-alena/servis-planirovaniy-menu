import sqlite3
from pathlib import Path
import django
from django.conf import settings


settings_module = "menu.settings"
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

django.setup()

from django.db import transaction
from dishes.models import Dish, DishIngredient
from ingredients.models import Ingredient
from meals.models import Meal


SOURCE_DB = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "cookbook.sqlite"
)


def import_data():
    """Перенести данные из старой базы."""

    source = sqlite3.connect(SOURCE_DB)
    source.row_factory = sqlite3.Row

    try:
        meals = source.execute(
            "SELECT id, name FROM meals ORDER BY id"
        ).fetchall()

        ingredients = source.execute(
            "SELECT id, name, unit FROM ingredients ORDER BY id"
        ).fetchall()

        dishes = source.execute(
            """
            SELECT id, name, calories, meal_id
            FROM dishes
            ORDER BY id
            """
        ).fetchall()

        relations = source.execute(
            """
            SELECT dish_id, ingredient_id
            FROM dish_ingredients
            ORDER BY dish_id, ingredient_id
            """
        ).fetchall()

    finally:
        source.close()

    if any([
        Meal.objects.exists(),
        Ingredient.objects.exists(),
        Dish.objects.exists(),
        DishIngredient.objects.exists(),
    ]):
        raise RuntimeError(
            "Целевая база уже содержит данные. Импорт остановлен."
        )

    with transaction.atomic():
        Meal.objects.bulk_create([
            Meal(id=row["id"], name=row["name"])
            for row in meals
        ])

        Ingredient.objects.bulk_create([
            Ingredient(
                id=row["id"],
                name=row["name"],
                unit=row["unit"],
            )
            for row in ingredients
        ])

        Dish.objects.bulk_create([
            Dish(
                id=row["id"],
                name=row["name"],
                calories=row["calories"],
                meal_id=row["meal_id"],
            )
            for row in dishes
        ])

        DishIngredient.objects.bulk_create([
            DishIngredient(
                dish_id=row["dish_id"],
                ingredient_id=row["ingredient_id"],
            )
            for row in relations
        ])

    print("Импорт завершён успешно!")
    print(f"Приёмы пищи: {Meal.objects.count()}")
    print(f"Ингредиенты: {Ingredient.objects.count()}")
    print(f"Блюда: {Dish.objects.count()}")
    print(f"Связи: {DishIngredient.objects.count()}")


if __name__ == "__main__":
    import_data()