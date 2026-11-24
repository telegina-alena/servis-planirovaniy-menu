
"""Представления для работы со страницами блюд."""

from django.shortcuts import render

from models.dishes import find_dish_by_id
from storage import (
    load_dishes,
    load_ingredients,
    ingredient_names,
)


def dishes(request):
    """Отобразить список всех блюд."""

    dishes_list = load_dishes()

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

    dishes_list = load_dishes()
    dish = find_dish_by_id(dishes_list, dish_id)

    availability_text = ""

    if dish is not None:
        ingredients_list = load_ingredients()

        availability_text = dish.is_available(
            ingredient_names(ingredients_list)
        )

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