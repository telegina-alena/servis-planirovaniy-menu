
"""Представления для работы со страницами приёмов пищи."""

from django.shortcuts import render

from models.meals import Meal


def meals(request):
    """Отобразить список доступных приёмов пищи."""

    available_meals = Meal.available_meals()

    context = {
        "meals": available_meals,
    }

    return render(
        request,
        "meals/meal_list.html",
        context,
    )


def meal_detail(request, meal_name):
    """Отобразить информацию о выбранном приёме пищи."""

    available_meals = Meal.available_meals()

    if meal_name.lower() not in available_meals:
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