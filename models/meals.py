"""Справочник приёмов пищи и подсказок по сервировке."""


class Meal:
    """Приём пищи с рекомендацией по сервировке."""

    _SUGGESTIONS = {
        "завтрак": "Подавать на маленькой тарелке",
        "обед": "Подавать на большой тарелке с гарниром",
        "ужин": "Подавать на средней тарелке",
    }

    def __init__(self, name: str) -> None:
        """Создать объект приёма пищи."""
        self.name = name.strip().lower()

    def __str__(self) -> str:
        return self.name

    def suggestion(self) -> str:
        """Вернуть рекомендацию по сервировке (метод из ПР1)."""
        return self._SUGGESTIONS.get(
            self.name, "Подавать на тарелке"
        )

    @classmethod
    def available_meals(cls) -> list[str]:
        """Вернуть список доступных приёмов пищи."""
        return list(cls._SUGGESTIONS.keys())