__author__ = 'panasco'

from django import forms as f
from django.contrib.auth.models import User

class LoginForm(f.ModelForm):
    username = f.CharField(max_length=200)
    password = f.PasswordInput()

    class Meta:
        model = User
        fields = ['username', 'password']