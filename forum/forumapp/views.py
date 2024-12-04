from django.shortcuts import render, redirect
from django.contrib import auth
from django.forms import ValidationError
from django.http import HttpRequest
from datetime import datetime
from .forms import Login, Create
from .models import Post

# Create your views here.

def get_posts():
    return Post.objects.reverse()[:5]

def index(request):
    return render(request, 'index.html',
                  {'posts': get_posts()})

def login(request):
    if request.method == 'POST':
        loginForm = Login(request.POST)
        if loginForm.is_valid():
            user = auth.authenticate(request, username=loginForm.cleaned_data['login'],
                                     password=loginForm.cleaned_data['password'])
            if user is not None:
                auth.login(request, user)
                return render(request, 'index.html',
                              {'posts': get_posts()})
            else:
                loginForm.add_error(None, ValidationError('Ошибка логина или пароля.'))
                return render(request, 'login.html',
                              {'form': loginForm,
                               'posts': get_posts()})
    else:
        loginForm = Login()
    return render(request, 'login.html',
                  {"form": loginForm,
                   'posts': get_posts()})

def create(request: HttpRequest):
    if request.method == 'POST':
        form = Create(request.POST)
        if form.is_valid():
            post = Post()
            post.title = form.cleaned_data.get('title')
            post.content = form.cleaned_data.get('content')
            post.author = request.user
            post.date = datetime.now()
            post.save()
            post = Post.objects.get(author=post.author,
                             date=post.date,
                             title=post.title)
            return redirect('view', postid=post.id)
    else:
        form = Create()
        return render(request, 'createpost.html',
                      {'form': form,
                       'posts': get_posts()})

def view(request, postid):
    post = Post.objects.get(id=postid)
    return render(request, 'viewpost.html',
                  {'post': post,
                   'posts': get_posts()})

def logout(request):
    auth.logout(request)
    return redirect('index')