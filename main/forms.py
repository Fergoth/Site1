from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

PERM = (("customer","Базовый пользователь"),
                       ("performer","Исполнитель"),
                       ("reviewer","Рецензент"),)

class SignUpForm(UserCreationForm):
    perm = forms.CharField(max_length=30,
        widget=forms.Select(choices=PERM), )

    class Meta:
        model = User
        fields = ("username", "perm", "password1", "password2")


