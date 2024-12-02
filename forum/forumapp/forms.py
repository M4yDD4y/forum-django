from django import forms
from .models import Post

class Login(forms.Form):
    login = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')

class Create(forms.Form):
    title = forms.CharField(max_length=100, label='Заголовок')
    content = forms.CharField(widget=forms.Textarea, label='Пост')