from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .forms import DishFilterForm
from .models import Dish
from ingredients.models import Ingredient
from meals.models import Meal
from django.shortcuts import redirect
from .forms import DishCreateForm


def dishes(request):
    """Отобразить список блюд с поиском и фильтрацией."""

    form = DishFilterForm(request.GET or None)

    form_valid = form.is_bound and form.is_valid()

    search_query = ""
    selected_meal = ""
    max_calories = ""
    sort = "name"
    error = None

    # Получаем параметры только после успешной проверки формы.
    if form_valid:
        search_query = form.cleaned_data.get("q", "").strip()

        meal = form.cleaned_data.get("meal")
        selected_meal = str(meal.pk) if meal else ""

        max_calories = form.cleaned_data.get("max_calories")
        sort = form.cleaned_data.get("sort") or "name"

    elif form.is_bound:
        error = "Проверьте корректность параметров фильтрации."

        # Сохраняем введённые значения для отображения.
        search_query = request.GET.get("q", "")
        selected_meal = request.GET.get("meal", "")
        max_calories = request.GET.get("max_calories", "")
        sort = request.GET.get("sort", "name")

    dishes_list = (
        Dish.objects
        .select_related("meal")
        .prefetch_related("ingredients")
    )

    # Фильтрация по приёму пищи.
    if form_valid and selected_meal:
        dishes_list = dishes_list.filter(
            meal_id=int(selected_meal)
        )

    # Фильтрация по калорийности.
    if form_valid and max_calories is not None:
        dishes_list = dishes_list.filter(
            calories__lte=max_calories
        )

    # Получаем объекты из базы.
    dishes_list = list(dishes_list)

    # Поиск с учётом регистра и кириллицы.
    if form_valid and search_query:
        normalized_query = search_query.casefold()

        dishes_list = [
            dish for dish in dishes_list
            if normalized_query in dish.name.casefold()
        ]

    # Сортировка.
    sort_functions = {
        "name": lambda dish: (
            dish.name.casefold(),
            dish.id,
        ),
        "calories": lambda dish: (
            dish.calories,
            dish.name.casefold(),
        ),
        "meal": lambda dish: (
            dish.meal.name.casefold(),
            dish.name.casefold(),
        ),
    }

    dishes_list.sort(
        key=sort_functions.get(
            sort,
            sort_functions["name"],
        )
    )

    # Пагинация.
    paginator = Paginator(dishes_list, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "dishes": page_obj,
        "page_obj": page_obj,
        "form": form,
        "search_query": search_query,
        "selected_meal": selected_meal,
        "max_calories": max_calories,
        "sort": sort,
        "meals": Meal.objects.order_by("name"),
        "error": error,
    }

    return render(
        request,
        "dishes/dish_list.html",
        context,
    )

def dish_detail(request, dish_id):
    """Отобразить подробную информацию о выбранном блюде."""

    dish = get_object_or_404(
        Dish.objects
        .select_related("meal")
        .prefetch_related("ingredients"),
        id=dish_id,
    )

    available_ingredients = Ingredient.objects.values_list(
        "name",
        flat=True,
    )

    availability_text = dish.is_available(
        available_ingredients
    )

    context = {
        "dish": dish,
        "availability_text": availability_text,
    }

    return render(
        request,
        "dishes/dish_detail.html",
        context,
    )


def dish_create(request):
    """Создать новое блюдо."""

    if request.method == "POST":
        form = DishCreateForm(request.POST)

        if form.is_valid():
            dish = form.save()
            return redirect(
                "dishes:detail",
                dish_id=dish.pk,
            )
    else:
        form = DishCreateForm()

    return render(
        request,
        "dishes/dish_form.html",
        {
            "form": form,
            "title": "Добавить блюдо",
        },
    )


def dish_update(request, dish_id):
    """Редактировать существующее блюдо."""

    dish = get_object_or_404(Dish, pk=dish_id)

    if request.method == "POST":
        form = DishCreateForm(
            request.POST,
            instance=dish,
        )

        if form.is_valid():
            dish = form.save()
            return redirect(
                "dishes:detail",
                dish_id=dish.pk,
            )
    else:
        form = DishCreateForm(instance=dish)

    return render(
        request,
        "dishes/dish_form.html",
        {
            "form": form,
            "title": "Редактировать блюдо",
            "dish": dish,
        },
    )