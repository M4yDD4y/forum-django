from django.shortcuts import render, redirect
from django.contrib import auth
from django.forms import ValidationError
from django.http import HttpRequest
from datetime import datetime
from .forms import Login, Create, Register, Comm
from .models import Post, User, Comment

# Create your views here.

def get_posts():
    return Post.objects.order_by("-id")[:5]

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
                return redirect('index')
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
    if request.method == "POST":
        form = Comm(request.POST)
        if form.is_valid():
            comm = Comment(content=form.cleaned_data.get('content'),
                        author=request.user,
                        date=datetime.now(),
                        post=post)
            comm.save()
            return redirect('view', postid=postid)
    comms = Comment.objects.filter(post=post)
    return render(request, 'viewpost.html',
                  {'post': post,
                   'comms': comms,
                   'form': Comm(),
                   'posts': get_posts()})

def logout(request):
    auth.logout(request)
    return redirect('index')

def register(request):
    if request.method == "POST":
        form = Register(request.POST)
        if form.is_valid():
            user = User(username=form.cleaned_data.get('login'))
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            return redirect('login')
        return render(request, 'registration.html',
                    {"form": form,
                    'posts': get_posts()})
    else:
        form = Register()
        return render(request, 'registration.html',
                    {"form": form,
                    'posts': get_posts()})