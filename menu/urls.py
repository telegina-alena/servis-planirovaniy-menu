
from django.conf import settings
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "",
        include(("homepage.urls", "homepage"), namespace="homepage"),
    ),

    path(
        "dishes/",
        include(("dishes.urls", "dishes"), namespace="dishes"),
    ),

    path(
        "ingredients/",
        include(("ingredients.urls", "ingredients"), namespace="ingredients"),
    ),

    path(
        "meals/",
        include(("meals.urls", "meals"), namespace="meals"),
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]


handler404 = "homepage.views.page_not_found"