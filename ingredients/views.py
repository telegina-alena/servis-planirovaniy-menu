
"""Представления для работы со страницами ингредиентов."""

from django.shortcuts import render

from db.database import get_connection


def ingredients(request):
    """Отобразить список всех ингредиентов."""

    conn = get_connection()

    try:
        ingredients_list = conn.execute(
            """
            SELECT
                id,
                name,
                unit
            FROM ingredients
            ORDER BY name
            """
        ).fetchall()

    finally:
        conn.close()

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

    conn = get_connection()

    try:
        ingredient = conn.execute(
            """
            SELECT
                id,
                name,
                unit
            FROM ingredients
            WHERE id = ?
            """,
            (ingredient_id,),
        ).fetchone()

    finally:
        conn.close()

    context = {
        "ingredient": ingredient,
    }

    return render(
        request,
        "ingredients/ingredient_detail.html",
        context,
        status=404 if ingredient is None else 200,
    )