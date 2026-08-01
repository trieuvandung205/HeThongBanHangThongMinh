from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path("", views.dashboard, name="dashboard"),

    # Chatbot
    path("chatbot/", views.chatbot_dashboard, name="chatbot_dashboard"),

    # Category
    path("categories/", views.category_list, name="category_list"),
    path("categories/add/", views.add_category, name="add_category"),
    path("categories/edit/<int:pk>/", views.edit_category, name="edit_category"),
    path("categories/delete/<int:pk>/", views.delete_category, name="delete_category"),

    # Orders
    path("orders/", views.order_list, name="order_list"),
    path("orders/<int:pk>/", views.update_order_status, name="update_order_status"),
    path("orders/detail/<int:pk>/", views.order_detail, name="order_detail"),

    # Users
    path("users/", views.user_list, name="user_list"),
    path("users/<int:pk>/", views.edit_user, name="edit_user"),
    path("users/add/", views.add_user, name="add_user"),
    path("users/<int:pk>/delete/", views.delete_user, name="delete_user"),

    # Staff
    path("staff/", views.staff_list, name="staff_list"),
    path("staff/add/", views.add_staff, name="add_staff"),
    path("staff/edit/<int:pk>/", views.edit_staff, name="edit_staff"),
    path("staff/delete/<int:pk>/", views.delete_staff, name="delete_staff"),
    path("chatbot/report/",    views.chatbot_report,    name="chatbot_report"),
    
]