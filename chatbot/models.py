from django.conf import settings
from django.db import models

from products.models import Product


class ChatHistory(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_history",
    )

    message = models.TextField()

    reply = models.TextField()

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = ["-created_at"]

    def __str__(self):

        return f"{self.user.username} - {self.created_at}"
class ChatFeedback(models.Model):

    chat = models.ForeignKey(
        ChatHistory,
        on_delete=models.CASCADE,
        related_name="feedbacks",
    )

    rating = models.PositiveSmallIntegerField()

    comment = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.rating}★"