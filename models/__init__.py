"""Пакет моделей предметной области «Кулинарная книга»."""
from .dishes import Dish
from .ingredients import Ingredient
from .meals import Meal

__all__ = ["Dish", "Ingredient", "Meal"]