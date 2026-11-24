from django.urls import path
from . import views


app_name = "dishes"

urlpatterns = [
    path("", views.dishes, name="list"),
    path("<int:dish_id>/", views.dish_detail, name="detail"),
    path("create/", views.dish_create, name="create"),
    path("<int:dish_id>/edit/", views.dish_update, name="edit"),
]