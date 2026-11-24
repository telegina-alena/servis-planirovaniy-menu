from django.shortcuts import render
from .models import Meal


MEAL_SLUGS = {
    "breakfast": "завтрак",
    "lunch": "обед",
    "dinner": "ужин",
}


def meals(request):
    """Отобразить список доступных приёмов пищи."""

    available_names = set(
        Meal.objects.values_list("name", flat=True)
    )

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

    meal = None

    if meal_name is not None:
        meal = Meal.objects.filter(
            name=meal_name
        ).first()

    context = {
        "meal": meal,
    }

    return render(
        request,
        "meals/meal_detail.html",
        context,
        status=404 if meal is None else 200,
    )