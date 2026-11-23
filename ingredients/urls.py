
from django.urls import path

from . import views


urlpatterns = [
    path("", views.ingredients, name="ingredients"),
    path(
        "<int:ingredient_id>/",
        views.ingredient_detail,
        name="ingredient_detail",
    ),
]
