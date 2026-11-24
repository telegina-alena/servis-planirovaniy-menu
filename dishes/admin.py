
from django.contrib import admin

from .models import Dish, DishIngredient


class DishIngredientInline(admin.TabularInline):
    model = DishIngredient
    extra = 1


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "calories",
        "meal",
    )

    list_display_links = ("name",)

    search_fields = (
        "name",
        "meal__name",
        "ingredients__name",
    )

    list_filter = ("meal",)

    ordering = ("name",)

    list_per_page = 20

    list_select_related = ("meal",)

    inlines = (DishIngredientInline,)
