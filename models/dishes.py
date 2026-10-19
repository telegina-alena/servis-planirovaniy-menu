from typing import Iterable

from .ingredients import Ingredient
from .meals import Meal


class Dish:

    def __init__(
        self,
        dish_id: int,
        name: str,
        ingredients: list[str],
        calories: int,
        meal: str,
    ) -> None:
        self.id = dish_id
        self.name = name
        self.ingredients = [i.strip().lower() for i in ingredients]
        self.calories = int(calories)
        self.meal = Meal(meal)

    def __str__(self) -> str:
        return (
            f"{self.name} ({self.calories} ккал, "
            f"{self.meal}, ингредиентов: {len(self.ingredients)})"
        )

    def __repr__(self) -> str:
        return f"Dish({self.id}, {self.name!r})"

    def is_available(self, available: Iterable[str]) -> str:
        available_set = {i.strip().lower() for i in available}
        missing = [i for i in self.ingredients if i not in available_set]
        if missing:
            return f"Не хватает ингредиентов: {', '.join(missing)}"
        return f"Все ингредиенты есть! Можно готовить {self.name}"

    def calories_per_portion(self, portions: int = 1) -> str:
        if portions <= 0:
            return "Количество порций должно быть больше нуля."
        per_portion = self.calories // portions
        level = self.calorie_level(per_portion)
        return f"{self.name} - {per_portion} ккал - {level}"

    @staticmethod
    def calorie_level(per_portion: int) -> str:
        if per_portion <= 200:
            return "легкое блюдо"
        if per_portion <= 400:
            return "средняя калорийность"
        return "калорийное блюдо"

    def serving_suggestion(self) -> str:
        return self.meal.suggestion()

    def uses_ingredient(self, ingredient_name: str) -> bool:
        return ingredient_name.strip().lower() in self.ingredients


    @classmethod
    def from_data(cls, data: dict) -> "Dish":
        return cls(
            dish_id=data["id"],
            name=data["name"],
            ingredients=data["ingredients"],
            calories=data["calories"],
            meal=data["meal"],
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "ingredients": self.ingredients,
            "calories": self.calories,
            "meal": self.meal.name,
        }

    @staticmethod
    def validate_calories(calories: int) -> bool:
        return isinstance(calories, int) and calories > 0

def add_dish(
    dishes: list[Dish],
    name: str,
    ingredients: list[str],
    calories: int,
    meal: str,
) -> Dish:
    new_id = max((d.id for d in dishes), default=0) + 1
    dish = Dish(new_id, name, ingredients, calories, meal)
    dishes.append(dish)
    return dish


def find_dish(dishes: list[Dish], query: str) -> list[Dish]:
    query = query.strip().lower()
    return [d for d in dishes if query in d.name.lower()]


def find_dish_by_id(dishes: list[Dish], dish_id: int) -> Dish | None:
    for dish in dishes:
        if dish.id == dish_id:
            return dish
    return None


def filter_dishes_by_meal(dishes: list[Dish], meal: str) -> list[Dish]:
    meal = meal.strip().lower()
    return [d for d in dishes if d.meal.name == meal]


def filter_dishes_by_calories(
    dishes: list[Dish], max_calories: int
) -> list[Dish]:
    return [d for d in dishes if d.calories <= max_calories]


def sort_dishes_by_calories(dishes: list[Dish]) -> list[Dish]:
    return sorted(dishes, key=lambda d: d.calories)


def show_dishes(dishes: list[Dish]) -> None:
    if not dishes:
        print("Список блюд пуст.")
        return
    header = f"{'ID':<4}{'Название':<25}{'Ккал':<8}{'Приём пищи':<12}"
    print(header)
    print("-" * 50)
    for d in dishes:
        print(f"{d.id:<4}{d.name:<25}{d.calories:<8}{d.meal:<12}")