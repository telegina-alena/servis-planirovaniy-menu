
from django.http import HttpResponse
from django.utils.html import escape

from homepage.views import page
from storage import load_ingredients


def ingredients(request):
    """Отобразить список всех ингредиентов."""

    ingredients_list = load_ingredients()

    items = ""

    for ingredient in ingredients_list:
        name = escape(ingredient.name)
        unit = escape(ingredient.unit)

        items += (
            '<li class="list-group-item">'
            f'<a href="/ingredients/{ingredient.id}/">'
            f'{name} ({unit})'
            '</a>'
            '</li>'
        )

    if not items:
        items = '<li class="list-group-item">Ингредиентов пока нет.</li>'

    content = f"""
    <h1 class="mb-3">Список ингредиентов</h1>

    <ul class="list-group">
        {items}
    </ul>
    """

    return HttpResponse(
        page(
            "Ингредиенты - Кулинарная книга",
            content,
            "ingredients"
        )
    )


def ingredient_detail(request, ingredient_id):
    """Отобразить подробную информацию об ингредиенте."""

    ingredients_list = load_ingredients()

    ingredient = next(
        (item for item in ingredients_list if item.id == ingredient_id),
        None
    )

    if ingredient is None:
        content = """
        <h1 class="text-danger">Ингредиент не найден</h1>

        <a href="/ingredients/" class="btn btn-outline-secondary">
            ← к списку ингредиентов
        </a>
        """

        return HttpResponse(
            page(
                "Ингредиент не найден",
                content,
                "ingredients"
            ),
            status=404
        )

    content = f"""
    <div class="card">
        <div class="card-body">
            <h2 class="card-title">{escape(ingredient.name)}</h2>

            <p class="card-text">
                <strong>ID:</strong> {ingredient.id}
            </p>

            <p class="card-text">
                <strong>Единица измерения:</strong>
                {escape(ingredient.unit)}
            </p>

            <a href="/ingredients/" class="btn btn-outline-secondary">
                ← к списку ингредиентов
            </a>
        </div>
    </div>
    """

    return HttpResponse(
        page(
            f"{escape(ingredient.name)} - Кулинарная книга",
            content,
            "ingredients"
        )
    )
