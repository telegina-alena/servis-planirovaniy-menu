from django.db import models
from django.core.validators import MinValueValidator
from ingredients.models import Ingredient
from meals.models import Meal


class Dish(models.Model):
    """Блюдо кулинарной книги."""

    name = models.CharField(
        max_length=200,
        verbose_name="Название",
    )

    calories = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Калорийность",
    )

    meal = models.ForeignKey(
        Meal,
        on_delete=models.PROTECT,
        related_name="dishes",
        verbose_name="Приём пищи",
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        through="DishIngredient",
        related_name="dishes",
        verbose_name="Ингредиенты",
    )

    def __str__(self):
        return f"{self.name} ({self.calories} ккал)"

    def is_available(self, available):
        """Проверить наличие всех ингредиентов."""

        available_set = {
            item.strip().lower() for item in available
        }

        missing = [
            ingredient.name
            for ingredient in self.ingredients.all()
            if ingredient.name.lower() not in available_set
        ]

        if missing:
            return f"Не хватает ингредиентов: {', '.join(missing)}"

        return f"Все ингредиенты есть! Можно готовить {self.name}"

    def calories_per_portion(self, portions=1):
        """Рассчитать калорийность одной порции."""

        if portions <= 0:
            return "Количество порций должно быть больше нуля."

        per_portion = self.calories // portions
        level = self.calorie_level(per_portion)

        return f"{self.name} - {per_portion} ккал - {level}"

    @staticmethod
    def calorie_level(per_portion):
        """Определить уровень калорийности."""

        if per_portion <= 200:
            return "легкое блюдо"

        if per_portion <= 400:
            return "средняя калорийность"

        return "калорийное блюдо"

    def serving_suggestion(self):
        """Получить рекомендацию по сервировке."""

        return self.meal.suggestion()

    def uses_ingredient(self, ingredient_name):
        """Проверить использование ингредиента."""

        return self.ingredients.filter(
            name__iexact=ingredient_name.strip()
        ).exists()

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"
        ordering = ["name"]


class DishIngredient(models.Model):
    """Промежуточная модель связи блюда и ингредиента."""

    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name="dish_ingredients",
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="dish_ingredients",
    )

    class Meta:
        verbose_name = "Ингредиент блюда"
        verbose_name_plural = "Ингредиенты блюд"

        constraints = [
            models.UniqueConstraint(
                fields=["dish", "ingredient"],
                name="unique_dish_ingredient",
            ),
        ]

    def __str__(self):
        return f"{self.dish.name} — {self.ingredient.name}"