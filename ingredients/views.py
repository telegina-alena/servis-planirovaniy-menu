
"""Представления для работы со страницами ингредиентов."""

from django.shortcuts import render

from storage import load_ingredients


def ingredients(request):
    """Отобразить список всех ингредиентов."""

    ingredients_list = load_ingredients()

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

    ingredients_list = load_ingredients()

    ingredient = next(
        (
            item for item in ingredients_list
            if item.id == ingredient_id
        ),
        None,
    )

    context = {
        "ingredient": ingredient,
    }

    return render(
        request,
        "ingredients/ingredient_detail.html",
        context,
        status=404 if ingredient is None else 200,
    )