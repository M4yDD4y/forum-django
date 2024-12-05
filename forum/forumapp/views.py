from django.shortcuts import render, redirect
from django.contrib import auth
from django.forms import ValidationError
from django.http import HttpRequest
from datetime import datetime
from .forms import Login, Create, Register, Comm, Search
from .models import Post, User, Comment, Topic

# Create your views here.


def get_posts():
    return Post.objects.order_by("-id")[:5]

def get_topics():
    return Topic.objects.order_by("-count")[:10]

def index(request):
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            search = form.cleaned_data.get("search")
            intitle = Post.objects.filter(title__icontains=search)
            incont = Post.objects.filter(content__icontains=search)
            result = intitle.union(incont)
            return render(request, 'index.html',
                  {'posts': get_posts(),
                   'topics': get_topics(),
                   'result': result,
                   'form': form})
    form = Search()
    return render(request, 'index.html',
                  {'posts': get_posts(),
                   'topics': get_topics(),
                   'form': form})

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
                               'posts': get_posts(),
                               'topics': get_topics()})
    else:
        loginForm = Login()
    return render(request, 'login.html',
                  {"form": loginForm,
                   'posts': get_posts(),
                   'topics': get_topics()})

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
            tags = form.cleaned_data.get('topics')
            for tag in tags.split(';'):
                if not Topic.objects.filter(name=tag).exists():
                    topic = Topic(name=tag)
                    topic.save()
                topic = Topic.objects.get(name=tag)
                post.topics.add(topic)
                topic.count += 1
                topic.save()
            post.save()
            post = Post.objects.get(author=post.author,
                             date=post.date,
                             title=post.title)
            return redirect('view', postid=post.id)
    else:
        form = Create()
        return render(request, 'createpost.html',
                      {'form': form,
                       'posts': get_posts(),
                       'topics': get_topics()})

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
                   'posts': get_posts(),
                   'topics': get_topics()})

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
                    'posts': get_posts(),
                    'topics': get_topics()})
    else:
        form = Register()
        return render(request, 'registration.html',
                    {"form": form,
                    'posts': get_posts(),
                    'topics': get_topics()})