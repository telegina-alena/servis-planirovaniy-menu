
from django.http import HttpResponse
from django.utils.html import escape

from homepage.views import page
from storage import (
    load_dishes,
    load_ingredients,
    ingredient_names,
)
from models.dishes import find_dish_by_id


def dishes(request):
    """Отобразить список всех блюд."""

    dishes_list = load_dishes()

    items = ""

    for dish in dishes_list:
        items += (
            '<li class="list-group-item">'
            f'<a href="/dishes/{dish.id}/">'
            f'<strong>{escape(dish.name)}</strong>'
            f' — Калорийность: {dish.calories} ккал, '
            f'приём пищи: {escape(str(dish.meal))}'
            '</a>'
            '</li>'
        )

    if not items:
        items = '<li class="list-group-item">Блюд пока нет.</li>'

    content = f"""
    <h1 class="mb-3">Список блюд</h1>

    <ul class="list-group">
        {items}
    </ul>
    """

    return HttpResponse(
        page(
            "Блюда - Кулинарная книга",
            content,
            "dishes"
        )
    )


def dish_detail(request, dish_id):
    """Отобразить подробную информацию о выбранном блюде."""

    dishes_list = load_dishes()
    dish = find_dish_by_id(dishes_list, dish_id)

    if dish is None:
        content = """
        <h1 class="text-danger">Блюдо не найдено</h1>

        <a href="/dishes/" class="btn btn-outline-secondary">
            ← к списку блюд
        </a>
        """

        return HttpResponse(
            page(
                "Блюдо не найдено",
                content,
                "dishes"
            ),
            status=404
        )

    ingredients_list = load_ingredients()

    availability_text = dish.is_available(
        ingredient_names(ingredients_list)
    )

    ingredients_text = ", ".join(dish.ingredients)

    content = f"""
    <div class="card">
        <div class="card-body">

            <h2 class="card-title">{escape(dish.name)}</h2>

            <p class="card-text">
                <strong>ID:</strong> {dish.id}
            </p>

            <p class="card-text">
                <strong>Калорийность:</strong> {dish.calories} ккал
            </p>

            <p class="card-text">
                <strong>Приём пищи:</strong> {escape(str(dish.meal))}
            </p>

            <p class="card-text">
                <strong>Ингредиенты:</strong>
                {escape(ingredients_text)}
            </p>

            <p class="card-text">
                <strong>Наличие ингредиентов:</strong>
                {escape(availability_text)}
            </p>

            <a href="/dishes/" class="btn btn-outline-secondary">
                ← к списку блюд
            </a>

        </div>
    </div>
    """

    return HttpResponse(
        page(
            f"{escape(dish.name)} - Кулинарная книга",
            content,
            "dishes"
        )
    )