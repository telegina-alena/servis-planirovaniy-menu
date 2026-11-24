
"""Представления для работы со страницами приёмов пищи."""

from django.shortcuts import render

from db.database import get_connection
from models.meals import Meal


MEAL_SLUGS = {
    "breakfast": "завтрак",
    "lunch": "обед",
    "dinner": "ужин",
}


def meals(request):
    """Отобразить список доступных приёмов пищи."""

    conn = get_connection()

    try:
        available_meals = conn.execute(
            "SELECT name FROM meals ORDER BY id"
        ).fetchall()

    finally:
        conn.close()

    available_names = {
        item["name"] for item in available_meals
    }

    meals_list = [
        {
            "slug": slug,
            "name": name,
        }
        for slug, name in MEAL_SLUGS.items()
        if name in available_names
    ]

    context = {
        "meals": meals_list,
    }

    return render(
        request,
        "meals/meal_list.html",
        context,
    )


def meal_detail(request, meal_slug):
    """Отобразить информацию о выбранном приёме пищи."""

    meal_name = MEAL_SLUGS.get(meal_slug)

    conn = get_connection()

    try:
        meal_data = None

        if meal_name is not None:
            meal_data = conn.execute(
                "SELECT id, name FROM meals WHERE name = ?",
                (meal_name,),
            ).fetchone()

    finally:
        conn.close()

    if meal_data is None:
        return render(
            request,
            "meals/meal_detail.html",
            {"meal": None},
            status=404,
        )

    meal = Meal(meal_data["name"])

    context = {
        "meal": meal,
    }

    return render(
        request,
        "meals/meal_detail.html",
        context,
    )