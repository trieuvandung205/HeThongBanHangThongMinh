from django import forms
from products.models import Product
from accounts.models import User


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = "__all__"


class UserForm(forms.ModelForm):

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"class":"form-control"})
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "role",
            "is_active",
        ]

        widgets = {
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "phone":forms.TextInput(attrs={"class":"form-control"}),
            "role":forms.Select(attrs={"class":"form-select"}),
        }