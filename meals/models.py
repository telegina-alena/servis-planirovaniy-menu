
"""Модель приёмов пищи."""

from django.db import models


class Meal(models.Model):
    """Приём пищи с рекомендацией по сервировке."""

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Название",
    )

    def __str__(self):
        return self.name

    def suggestion(self):
        """Вернуть рекомендацию по сервировке."""

        suggestions = {
            "завтрак": "Подавать на маленькой тарелке",
            "обед": "Подавать на большой тарелке с гарниром",
            "ужин": "Подавать на средней тарелке",
        }

        return suggestions.get(
            self.name,
            "Подавать на тарелке",
        )

    class Meta:
        verbose_name = "Приём пищи"
        verbose_name_plural = "Приёмы пищи"
        ordering = ["id"]
