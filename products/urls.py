from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path(
        "products/",
        views.product_list,
        name="product_list",
    ),

    path(
        "products/category/<int:pk>/",
        views.category,
        name="category",
    ),

    path(
        "products/search/",
        views.search,
        name="search",
    ),
    path(
    "products/suggest/",
    views.search_suggest,
    name="search_suggest",
    ),

    path(
        "product/<slug:slug>/",
        views.product_detail,
        name="product_detail",
    ),
]