
"""Представления для работы со страницами блюд."""

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from .models import Dish
from ingredients.models import Ingredient
from meals.models import Meal


def dishes(request):
    """Отобразить список блюд с поиском и фильтрацией."""

    search_query = request.GET.get("q", "").strip()
    selected_meal = request.GET.get("meal", "").strip()
    max_calories = request.GET.get("max_calories", "").strip()
    sort = request.GET.get("sort", "name")

    dishes_list = (
        Dish.objects
        .select_related("meal")
        .prefetch_related("ingredients")
    )

    # Поиск по названию с учётом кириллицы.
    # SQLite не обеспечивает полноценный Unicode case-insensitive LIKE.
    if search_query:
        normalized_query = search_query.casefold()

        dishes_list = [
            dish for dish in dishes_list
            if normalized_query in dish.name.casefold()
        ]

    # Фильтрация по приёму пищи.
    if selected_meal.isdigit():
        dishes_list = dishes_list.filter(
            meal_id=int(selected_meal)
        ) if hasattr(dishes_list, "filter") else [
            dish for dish in dishes_list
            if dish.meal_id == int(selected_meal)
        ]

    # Фильтрация по калорийности.
    error = None

    if max_calories:
        try:
            calories_limit = int(max_calories)
            if calories_limit < 0:
                raise ValueError
        except ValueError:
            error = "Укажите корректное количество калорий."
        else:
            dishes_list = (
                dishes_list.filter(calories__lte=calories_limit)
                if hasattr(dishes_list, "filter")
                else [
                    dish for dish in dishes_list
                    if dish.calories <= calories_limit
                ]
            )

    # Сортировка средствами Django ORM.
    sort_fields = {
        "name": ("name", "id"),
        "calories": ("calories", "name"),
        "meal": ("meal__name", "name"),
    }

    if hasattr(dishes_list, "order_by"):
        dishes_list = dishes_list.order_by(
            *sort_fields.get(sort, sort_fields["name"])
        )
    else:
        sort_keys = {
            "name": lambda dish: (dish.name.casefold(), dish.id),
            "calories": lambda dish: (dish.calories, dish.name.casefold()),
            "meal": lambda dish: (
                dish.meal.name.casefold(),
                dish.name.casefold(),
            ),
        }
        dishes_list.sort(
            key=sort_keys.get(sort, sort_keys["name"])
        )

    # Пагинация.
    paginator = Paginator(dishes_list, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "dishes": page_obj,
        "page_obj": page_obj,
        "search_query": search_query,
        "selected_meal": selected_meal,
        "max_calories": max_calories,
        "sort": sort,
        "meals": Meal.objects.order_by("name"),
        "error": error,
    }

    return render(
        request,
        "dishes/dish_list.html",
        context,
    )


def dish_detail(request, dish_id):
    """Отобразить подробную информацию о выбранном блюде."""

    dish = get_object_or_404(
        Dish.objects
        .select_related("meal")
        .prefetch_related("ingredients"),
        id=dish_id,
    )

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
    )