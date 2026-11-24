from django.shortcuts import render
from .models import Dish
from ingredients.models import Ingredient


def dishes(request):
    """Отобразить список всех блюд."""

    dishes_list = (
        Dish.objects
        .select_related("meal")
        .prefetch_related("ingredients")
        .all()
    )

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

    dish = (
        Dish.objects
        .select_related("meal")
        .prefetch_related("ingredients")
        .filter(id=dish_id)
        .first()
    )

    availability_text = ""

    if dish is not None:
        available_ingredients = Ingredient.objects.values_list(
            "name",
            flat=True,
        )

        availability_text = dish.is_available(
            available_ingredients
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