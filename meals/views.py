from django.shortcuts import render
from models.meals import Meal


MEAL_SLUGS = {
    "breakfast": "завтрак",
    "lunch": "обед",
    "dinner": "ужин",
}


def meals(request):
    """Отобразить список доступных приёмов пищи."""

    available_meals = Meal.available_meals()

    meals_list = [
        {
            "slug": slug,
            "name": name,
        }
        for slug, name in MEAL_SLUGS.items()
        if name in available_meals
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

    if meal_name not in Meal.available_meals():
        return render(
            request,
            "meals/meal_detail.html",
            {"meal": None},
            status=404,
        )

    meal = Meal(meal_name)

    context = {
        "meal": meal,
    }

    return render(
        request,
        "meals/meal_detail.html",
        context,
    )