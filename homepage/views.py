
"""Представления главной страницы, статистики и ошибок."""

from django.shortcuts import render
from django.db.models import Avg, Count, F

from dishes.models import Dish
from ingredients.models import Ingredient
from meals.models import Meal


def index(request):
    """Главная страница проекта."""

    return render(request, "homepage/index.html")


def statistics(request):
    """Отобразить статистику кулинарной книги."""

    dishes_count = Dish.objects.count()

    ingredients_count = Ingredient.objects.count()

    average_calories = (
        Dish.objects.aggregate(
            average=Avg("calories")
        )["average"] or 0
    )

    meals_statistics = list(
        Meal.objects
        .annotate(dishes_count=Count("dishes"))
        .values(
            "dishes_count",
            meal_name=F("name"),
        )
    )

    ingredients_statistics = list(
        Ingredient.objects
        .annotate(dishes_count=Count("dishes", distinct=True))
        .values(
            "dishes_count",
            ingredient_name=F("name"),
        )
        .order_by("-dishes_count", "ingredient_name")
    )

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