
"""Представления для работы со страницами блюд."""

from django.shortcuts import render

from db.database import get_connection


def dishes(request):
    """Отобразить список всех блюд."""

    conn = get_connection()

    try:
        dishes_list = conn.execute(
            """
            SELECT
                dishes.id,
                dishes.name,
                dishes.calories,
                meals.name AS meal
            FROM dishes
            JOIN meals ON dishes.meal_id = meals.id
            ORDER BY dishes.name
            """
        ).fetchall()

    finally:
        conn.close()

    context = {
        "dishes": dishes_list,
    }

    return render(
        request,
        "dishes/dish_list.html",
        context,
    )


def dish_detail(request, dish_id):
    """Отобразить подробную информацию о выбранном блюде."""

    conn = get_connection()

    try:
        dish = conn.execute(
            """
            SELECT
                dishes.id,
                dishes.name,
                dishes.calories,
                meals.name AS meal
            FROM dishes
            JOIN meals ON dishes.meal_id = meals.id
            WHERE dishes.id = ?
            """,
            (dish_id,),
        ).fetchone()

        if dish is not None:
            ingredients = conn.execute(
                """
                SELECT ingredients.name
                FROM ingredients
                JOIN dish_ingredients
                    ON ingredients.id = dish_ingredients.ingredient_id
                WHERE dish_ingredients.dish_id = ?
                ORDER BY ingredients.name
                """,
                (dish_id,),
            ).fetchall()

            ingredient_list = [
                item["name"] for item in ingredients
            ]

            available = {
                item["name"]
                for item in conn.execute(
                    "SELECT name FROM ingredients"
                ).fetchall()
            }

            missing = [
                name
                for name in ingredient_list
                if name not in available
            ]

            dish = dict(dish)
            dish["ingredients"] = ingredient_list

            if missing:
                availability_text = (
                    "Не хватает ингредиентов: "
                    + ", ".join(missing)
                )
            else:
                availability_text = (
                    f"Все ингредиенты есть! "
                    f"Можно готовить {dish['name']}"
                )

        else:
            availability_text = ""

    finally:
        conn.close()

    context = {
        "dish": dish,
        "availability_text": availability_text,
    }

    return render(
        request,
        "dishes/dish_detail.html",
        context,
        status=404 if dish is None else 200,
    )