
from django.contrib import admin

from .models import Meal


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )

    search_fields = ("name",)

    ordering = ("id",)

    list_per_page = 20
