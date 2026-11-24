
from django.contrib import admin

from .models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "unit",
    )

    search_fields = ("name",)

    list_filter = ("unit",)

    ordering = ("name",)

    list_per_page = 20