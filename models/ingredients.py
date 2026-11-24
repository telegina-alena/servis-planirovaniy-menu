"""Класс ингредиента."""


class Ingredient:
    """Ингредиент, доступный на кухне."""

    def __init__(self, ingredient_id: int, name: str, unit: str = "шт") -> None:
        """Создать объект ингредиента."""
        self.id = ingredient_id
        self.name = name.strip().lower()
        self.unit = unit.strip()

    def __str__(self) -> str:
        """Строковое представление ингредиента."""
        return f"{self.name} ({self.unit})"

    def __repr__(self) -> str:
        return f"Ingredient({self.id}, {self.name!r}, {self.unit!r})"

    @classmethod
    def from_data(cls, data: dict) -> "Ingredient":
        """Создать ингредиент из словаря (например, из JSON)."""
        return cls(
            ingredient_id=data["id"],
            name=data["name"],
            unit=data.get("unit", "шт"),
        )

    def to_dict(self) -> dict:
        """Преобразовать объект в словарь для сохранения в JSON."""
        return {"id": self.id, "name": self.name, "unit": self.unit}

    @staticmethod
    def validate_name(name: str) -> bool:
        """Проверить, что название ингредиента корректно."""
        return bool(name and name.strip())