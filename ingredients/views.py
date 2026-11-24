from django.shortcuts import render
from .models import Ingredient


def ingredients(request):
    """Отобразить список всех ингредиентов."""

    ingredients_list = Ingredient.objects.all()

    context = {
        "ingredients": ingredients_list,
    }

    return render(
        request,
        "ingredients/ingredient_list.html",
        context,
    )


def ingredient_detail(request, ingredient_id):
    """Отобразить подробную информацию об ингредиенте."""

    ingredient = Ingredient.objects.filter(
        id=ingredient_id
    ).first()

    context = {
        "ingredient": ingredient,
    }

    return render(
        request,
        "ingredients/ingredient_detail.html",
        context,
        status=404 if ingredient is None else 200,
    )