from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="staff_dashboard"),

    # Products
    path("products/", views.product_list, name="staff_product_list"),
    path("products/add/", views.add_product, name="staff_add_product"),
    path("products/<int:pk>/edit/", views.edit_product, name="staff_edit_product"),
    path("products/<int:pk>/delete/", views.delete_product, name="staff_delete_product"),

    # Orders
    path("orders/", views.order_list, name="staff_order_list"),
    path("orders/<int:pk>/", views.order_detail, name="staff_order_detail"),
    path("orders/<int:pk>/update/", views.update_order, name="staff_update_order"),

    # Profile
    path("profile/", views.profile, name="staff_profile"),
    path("password/", views.change_password, name="staff_change_password"),
]