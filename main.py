"""Точка запуска приложения «Кулинарная книга»."""
from models import Dish, Ingredient
from models.dishes import (
    add_dish,
    filter_dishes_by_meal,
    find_dish,
    find_dish_by_id,
    show_dishes,
    sort_dishes_by_calories,
)
from storage import (
    ingredient_names,
    load_dishes,
    load_ingredients,
    save_dishes,
)
from utils import input_int, input_non_empty


def show_ingredients(ingredients: list[Ingredient]) -> None:
    """Вывести доступные ингредиенты (объекты Ingredient)."""
    if not ingredients:
        print("Список ингредиентов пуст.")
        return
    print("Доступные ингредиенты:")
    for ing in ingredients:
        print(f"  [{ing.id}] {ing}")


def menu_add_dish(dishes: list[Dish]) -> None:
    """Сценарий добавления блюда."""
    name = input_non_empty("Название блюда: ")
    raw = input_non_empty("Ингредиенты через запятую: ")
    ingredients = [i.strip() for i in raw.split(",") if i.strip()]
    calories = input_int("Калорийность (ккал): ")
    meal = input_non_empty("Приём пищи (завтрак/обед/ужин): ")
    dish = add_dish(dishes, name, ingredients, calories, meal)
    print(f"Блюдо добавлено с ID={dish.id}.")


def menu_find_dish(dishes: list[Dish]) -> None:
    """Сценарий поиска блюда по названию."""
    query = input_non_empty("Подстрока для поиска: ")
    show_dishes(find_dish(dishes, query))


def menu_check_availability(
    dishes: list[Dish], ingredients: list[Ingredient]
) -> None:
    """Сценарий проверки наличия ингредиентов (метод Dish)."""
    dish_id = input_int("ID блюда: ")
    dish = find_dish_by_id(dishes, dish_id)
    if dish is None:
        print("Блюдо с таким ID не найдено.")
        return
    print(dish.is_available(ingredient_names(ingredients)))


def menu_calories(dishes: list[Dish]) -> None:
    """Сценарий расчёта калорий на порцию (метод Dish)."""
    dish_id = input_int("ID блюда: ")
    dish = find_dish_by_id(dishes, dish_id)
    if dish is None:
        print("Блюдо с таким ID не найдено.")
        return
    portions = input_int("Количество порций: ")
    print(dish.calories_per_portion(portions))


def menu_suggestion(dishes: list[Dish]) -> None:
    """Сценарий подсказки по сервировке (метод Dish)."""
    dish_id = input_int("ID блюда: ")
    dish = find_dish_by_id(dishes, dish_id)
    if dish is None:
        print("Блюдо с таким ID не найдено.")
        return
    print(dish.serving_suggestion())


def menu_filter_by_meal(dishes: list[Dish]) -> None:
    """Сценарий отбора блюд по приёму пищи."""
    meal = input_non_empty("Приём пищи (завтрак/обед/ужин): ")
    show_dishes(filter_dishes_by_meal(dishes, meal))


def menu_sort_by_calories(dishes: list[Dish]) -> None:
    """Сценарий сортировки блюд по калорийности."""
    show_dishes(sort_dishes_by_calories(dishes))


def main() -> None:
    """Точка входа: загрузка данных и цикл меню."""
    dishes: list[Dish] = load_dishes()
    ingredients: list[Ingredient] = load_ingredients()

    actions = {
        "1": ("Показать все блюда", lambda: show_dishes(dishes)),
        "2": ("Показать ингредиенты",
              lambda: show_ingredients(ingredients)),
        "3": ("Найти блюдо по названию", lambda: menu_find_dish(dishes)),
        "4": ("Отобрать по приёму пищи",
              lambda: menu_filter_by_meal(dishes)),
        "5": ("Отсортировать по калорийности",
              lambda: menu_sort_by_calories(dishes)),
        "6": ("Проверить наличие ингредиентов",
              lambda: menu_check_availability(dishes, ingredients)),
        "7": ("Рассчитать калории на порцию",
              lambda: menu_calories(dishes)),
        "8": ("Подсказать сервировку",
              lambda: menu_suggestion(dishes)),
        "9": ("Добавить блюдо", lambda: menu_add_dish(dishes)),
    }

    print("== Кулинарная книга ==")
    while True:
        print()
        for key, (title, _) in actions.items():
            print(f"{key}. {title}")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()
        if choice == "0":
            save_dishes(dishes)
            print("Данные сохранены. До встречи!")
            break

        action = actions.get(choice)
        if action is None:
            print("Неизвестная команда, попробуйте снова.")
            continue
        action[1]()


if __name__ == "__main__":
    main()