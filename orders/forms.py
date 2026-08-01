from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):

    class Meta:
        model = Order

        fields = [
            "full_name",
            "phone",
            "address",
            "note",
        ]

        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập họ và tên",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập số điện thoại",
                }
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Nhập địa chỉ giao hàng",
                }
            ),
            "note": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Ghi chú (không bắt buộc)",
                }
            ),
        }