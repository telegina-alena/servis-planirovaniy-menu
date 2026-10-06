from django.contrib import admin
from django.urls import include, path

urlpatterns = [
 path("admin/", admin.site.urls),
 path("", include("homepage.urls")),
 path("dishes/", include("dishes.urls")),
 path("ingredients/", include("ingredients.urls")),
 path("meals/", include("meals.urls")),
]
