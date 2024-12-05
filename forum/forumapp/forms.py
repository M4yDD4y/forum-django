from typing import Any
from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import Post, User

class Login(forms.Form):
    login = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')

class Create(forms.Form):
    title = forms.CharField(max_length=100, label='Заголовок')
    topics = forms.CharField(label="Тематики", help_text="Введите тэги длиной не более 50 символов через ;", required=False)
    content = forms.CharField(widget=forms.Textarea, label='Пост')

    def clean(self):
        cleaned_data = super().clean()
        tags = cleaned_data.get("topics")
        if any([len(t) > 50 for t in tags.split(";")]):
            raise forms.ValidationError("Тэги слишком длинные.")

class Register(forms.Form):
    login = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    pconfirm = forms.CharField(widget=forms.PasswordInput(), label='Повтор пароля')

    def clean(self):
        cleaned_data = super().clean()
        if User.objects.filter(username=cleaned_data.get('login')).exists():
            raise forms.ValidationError("Логин занят.")
        password = cleaned_data.get('password')
        pconfirm = cleaned_data.get('pconfirm')
        if password != pconfirm:
            raise forms.ValidationError("Пароли не совпадают.")
        validate_password(password)

class Comm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Оставить комментарий")

class Search(forms.Form):
    search = forms.CharField(label="")