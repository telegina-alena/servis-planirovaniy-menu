from django.http import HttpResponse

from models.meals import Meal


def meals(request):
    available_meals = Meal.available_meals()
    content = ", ".join(available_meals)

    return HttpResponse(f"Доступные приёмы пищи: {content}")


def meal_detail(request, meal_name):
    meal = Meal(meal_name)

    return HttpResponse(
        f"{meal.name.capitalize()}: {meal.suggestion()}"
    )
