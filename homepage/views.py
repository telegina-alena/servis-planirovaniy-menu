
from django.http import HttpResponse


def page(title, content, active_page=None):
    """Формирует общую HTML-страницу с навигацией."""

    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/"
        "dist/css/bootstrap.min.css"
    )

    def nav_link(label, url, key):
        active = active_page == key

        css_class = "nav-link"
        if active:
            css_class += " active fw-semibold"

        aria = ' aria-current="page"' if active else ""

        return (
            f'<a class="{css_class}" href="{url}"{aria}>'
            f'{label}</a>'
        )

    navigation = f"""
    <nav class="navbar navbar-expand bg-light border-bottom mb-4">
        <div class="container">
            <div class="navbar-nav">
                {nav_link("Главная", "/", "home")}
                {nav_link("Блюда", "/dishes/", "dishes")}
                {nav_link("Ингредиенты", "/ingredients/", "ingredients")}
                {nav_link("Приёмы пищи", "/meals/", "meals")}
            </div>
        </div>
    </nav>
    """

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
    <style>
        .nav-link.active {{
            color: #0d6efd !important;
            border-bottom: 2px solid #0d6efd;
        }}

        main {{
            max-width: 900px;
        }}
    </style>
</head>
<body>
    {navigation}

    <main class="container">
        {content}
    </main>
</body>
</html>"""


def index(request):
    """Главная страница проекта."""

    content = """
    <h1 class="display-5">Кулинарная книга</h1>

    <p class="lead">
        Сервис планирования меню и расчёта калорий.
    </p>

    <p>Выберите интересующий вас раздел:</p>

    <a href="/dishes/" class="btn btn-primary me-2">
        Блюда
    </a>

    <a href="/ingredients/" class="btn btn-outline-primary">
        Ингредиенты
    </a>
    """

    return HttpResponse(
        page(
            "Главная - Кулинарная книга",
            content,
            "home"
        )
    )


def page_not_found(request, exception):
    """Страница ошибки 404."""

    content = """
    <h1 class="text-danger">404 — Страница не найдена</h1>

    <p>Проверьте адрес или вернитесь на главную.</p>

    <a href="/" class="btn btn-primary">
        На главную
    </a>
    """

    return HttpResponse(
        page("404 - Не найдено", content),
        status=404
    )
