from django.urls import path
from . import views


app_name = "meals"

urlpatterns = [
    path("", views.meals, name="meals"),
    path("<slug:meal_slug>/", views.meal_detail, name="meal_detail"),
]