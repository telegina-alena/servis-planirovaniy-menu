
from django.http import HttpResponse
from django.utils.html import escape

from homepage.views import page
from models.meals import Meal


def meals(request):
    """Отобразить список доступных приёмов пищи."""

    available_meals = Meal.available_meals()

    items = ""

    for meal_name in available_meals:
        items += (
            '<li class="list-group-item">'
            f'<a href="/meals/{meal_name}/">'
            f'{escape(meal_name.capitalize())}'
            '</a>'
            '</li>'
        )

    content = f"""
    <h1 class="mb-3">Приёмы пищи</h1>

    <p>Выберите интересующий вас приём пищи:</p>

    <ul class="list-group">
        {items}
    </ul>
    """

    return HttpResponse(
        page(
            "Приёмы пищи - Кулинарная книга",
            content,
            "meals"
        )
    )


def meal_detail(request, meal_name):
    """Отобразить информацию о выбранном приёме пищи."""

    available_meals = Meal.available_meals()

    if meal_name.lower() not in available_meals:
        content = """
        <h1 class="text-danger">Приём пищи не найден</h1>

        <a href="/meals/" class="btn btn-outline-secondary">
            ← к списку приёмов пищи
        </a>
        """

        return HttpResponse(
            page(
                "Приём пищи не найден",
                content,
                "meals"
            ),
            status=404
        )

    meal = Meal(meal_name)

    content = f"""
    <div class="card">
        <div class="card-body">

            <h2 class="card-title">
                {escape(meal.name.capitalize())}
            </h2>

            <p class="card-text">
                <strong>Рекомендация по сервировке:</strong>
                {escape(meal.suggestion())}
            </p>

            <a href="/meals/" class="btn btn-outline-secondary">
                ← к списку приёмов пищи
            </a>

        </div>
    </div>
    """

    return HttpResponse(
        page(
            f"{meal.name.capitalize()} - Кулинарная книга",
            content,
            "meals"
        )
    )