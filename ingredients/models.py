from django.db import models


class Ingredient(models.Model):
    """Ингредиент, доступный на кухне."""

    name = models.CharField(
        max_length=100,
        verbose_name="Название",
    )

    unit = models.CharField(
        max_length=20,
        default="шт",
        verbose_name="Единица измерения",
    )

    def __str__(self):
        return f"{self.name} ({self.unit})"

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ["name"]