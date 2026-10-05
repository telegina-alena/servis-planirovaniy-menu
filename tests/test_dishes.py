"""Тесты класса Dish и функций работы с блюдами."""
from models import Dish
from models.dishes import (
    add_dish,
    filter_dishes_by_meal,
    find_dish,
    find_dish_by_id,
    sort_dishes_by_calories,
)


def _sample_dish() -> Dish:
    return Dish(1, "Курица с рисом", ["рис", "курица"], 200, "обед")


def test_dish_creation():
    dish = _sample_dish()
    assert dish.id == 1
    assert dish.name == "Курица с рисом"
    assert dish.calories == 200
    assert dish.meal.name == "обед"


def test_dish_str():
    dish = _sample_dish()
    assert "Курица с рисом" in str(dish)
    assert "200 ккал" in str(dish)


def test_dish_is_available_ok():
    dish = _sample_dish()
    result = dish.is_available(["рис", "курица", "соль"])
    assert "Можно готовить" in result


def test_dish_is_available_missing():
    dish = _sample_dish()
    result = dish.is_available(["рис"])
    assert "курица" in result


def test_dish_calories_per_portion():
    dish = _sample_dish()
    assert "100 ккал" in dish.calories_per_portion(2)
    assert "легкое" in dish.calories_per_portion(2)


def test_dish_serving_suggestion():
    dish = _sample_dish()
    assert "большой" in dish.serving_suggestion()


def test_add_dish():
    dishes: list[Dish] = []
    add_dish(dishes, "Омлет", ["яйца"], 150, "завтрак")
    assert len(dishes) == 1
    assert dishes[0].id == 1


def test_find_dish():
    dishes: list[Dish] = []
    add_dish(dishes, "Курица с рисом", ["рис"], 200, "обед")
    add_dish(dishes, "Омлет", ["яйца"], 150, "завтрак")
    assert len(find_dish(dishes, "куриц")) == 1
    assert find_dish(dishes, "торт") == []


def test_find_dish_by_id():
    dishes: list[Dish] = []
    add_dish(dishes, "Омлет", ["яйца"], 150, "завтрак")
    assert find_dish_by_id(dishes, 1) is not None
    assert find_dish_by_id(dishes, 99) is None


def test_filter_dishes_by_meal():
    dishes: list[Dish] = []
    add_dish(dishes, "Омлет", ["яйца"], 150, "завтрак")
    add_dish(dishes, "Салат", ["овощи"], 90, "ужин")
    assert len(filter_dishes_by_meal(dishes, "ужин")) == 1


def test_sort_dishes_by_calories():
    dishes: list[Dish] = []
    add_dish(dishes, "Тяжелое", ["x"], 500, "обед")
    add_dish(dishes, "Легкое", ["y"], 100, "завтрак")
    sorted_dishes = sort_dishes_by_calories(dishes)
    assert sorted_dishes[0].calories == 100