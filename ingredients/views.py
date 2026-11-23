
from django.http import HttpResponse


def ingredients(request):
    return HttpResponse("Список ингредиентов")


def ingredient_detail(request, ingredient_id):
    return HttpResponse(f"Ингредиент {ingredient_id}")
