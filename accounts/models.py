from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ROLE_CHOICES = [
        ("admin", "Quản trị viên"),
        ("staff", "Nhân viên"),
        ("customer", "Khách hàng"),
    ]

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="customer"
    )

    def is_admin(self):
        return self.role == "admin"

    def is_staff_user(self):
        return self.role == "staff"

    def is_customer(self):
        return self.role == "customer"

    def __str__(self):
        return self.username