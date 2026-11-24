
from django.urls import path

from . import views


urlpatterns = [
    path("", views.meals, name="meals"),
    path("<str:meal_name>/", views.meal_detail, name="meal_detail"),
]