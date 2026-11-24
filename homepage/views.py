from django.shortcuts import render
from db.database import get_connection


def index(request):
    return render(request, "homepage/index.html")


def statistics(request):
    
    conn = get_connection()

    try:
        dishes_count = conn.execute(
            "SELECT COUNT(*) FROM dishes"
        ).fetchone()[0]

        ingredients_count = conn.execute(
            "SELECT COUNT(*) FROM ingredients"
        ).fetchone()[0]

        average_calories = conn.execute(
            "SELECT COALESCE(AVG(calories), 0) FROM dishes"
        ).fetchone()[0]

        meals_statistics = [
            dict(row)
            for row in conn.execute(
                """
                SELECT
                    meals.name AS meal_name,
                    COUNT(dishes.id) AS dishes_count
                FROM meals
                LEFT JOIN dishes
                    ON meals.id = dishes.meal_id
                GROUP BY meals.id, meals.name
                ORDER BY meals.id
                """
            ).fetchall()
        ]

        ingredients_statistics = [
            dict(row)
            for row in conn.execute(
                """
                SELECT
                    ingredients.name AS ingredient_name,
                    COUNT(dish_ingredients.dish_id) AS dishes_count
                FROM ingredients
                LEFT JOIN dish_ingredients
                    ON ingredients.id = dish_ingredients.ingredient_id
                GROUP BY ingredients.id, ingredients.name
                ORDER BY dishes_count DESC, ingredients.name
                """
            ).fetchall()
        ]

    finally:
        conn.close()

    context = {
        "dishes_count": dishes_count,
        "ingredients_count": ingredients_count,
        "average_calories": round(average_calories, 1),
        "meals_statistics": meals_statistics,
        "ingredients_statistics": ingredients_statistics,
    }

    return render(
        request,
        "homepage/statistics.html",
        context,
    )


def page_not_found(request, exception):
    """Страница ошибки 404."""

    return render(
        request,
        "404.html",
        status=404,
    )