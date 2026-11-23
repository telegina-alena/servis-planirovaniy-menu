from django.http import HttpResponse
from django.shortcuts import render


def page(title, content):
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/"
        "dist/css/bootstrap.min.css"
    )

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav bg-light p-3 mb-4">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/dishes/">Блюда</a>
        <a class="nav-link" href="/ingredients/">Ингредиенты</a>
    </nav>
    <main class="container">
        {content}
    </main>
</body>
</html>"""


def index(request):
    return render(request, 'homepage/index.html')


def page_not_found(request, exception):
    content = """
    <h1 class="text-danger">404 - страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """

    return HttpResponse(
        page("404 - Не найдено", content),
        status=404
    )