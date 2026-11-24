
"""Представления главной страницы и обработки ошибок."""

from django.shortcuts import render


def index(request):
    """Главная страница проекта."""

    return render(request, "homepage/index.html")


def page_not_found(request, exception):
    """Страница ошибки 404."""

    return render(
        request,
        "404.html",
        status=404,
    )