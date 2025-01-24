from django.shortcuts import render, redirect
from django.contrib import auth
from django.forms import ValidationError
from django.http import HttpRequest
from datetime import datetime
from .forms import Login, Create, Register, Comm, Search
from .models import Post, User, Comment, Topic
from .models import Post, Comment
from .serializers import PostSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets

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
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

# class PostView(viewsets.ModelViewSet):
#     serializer_class = PostSerializer
#     queryset = Post.objects.all()

    # def list(self, request):
    #     queryset = Post.objects.all()
    #     serializer = PostSerializer(queryset, many=True)
    #     return Response(serializer.data)
    
    # def retrieve(self, request, pk=None):
    #     queryset = Post.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = PostSerializer(user)
    #     return Response(serializer.data)

    # def perform_create(self, serializer):
    #     comment = get_object_or_404(Comment, id=self.request.data.get('comment_id'))
    #     return serializer.save(comment=comment)

    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)
        # posts = Post.objects.all()
        # serializer = PostSerializer(posts, many=True)
        # return Response({"posts": serializer.data})
    
    

    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)
        # post = request.data.get("posts")
        # serializer = PostSerializer(data=post)
        # if serializer.is_valid(raise_exception=True):
        #     savedpost = serializer.save()
        # return Response({"success": "Article '{}' created successfully".format(savedpost.title)})
    
    def put(self, request, pk):
        post_saved = get_object_or_404(Post.objects.all(), pk=pk)
        data = request.data.get('posts')
        serializer = PostSerializer(instance=post_saved, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            post_saved = serializer.save()

        return Response({
            "success":"Article '{}' updated successfully".format(post_saved.title)
        })
    
    def delete(self, request, pk):
        post = get_object_or_404(Post.objects.all(), pk=pk)
        post.delete()
        return Response({
            "message": "Post with i '{}' has been deleted.".format(pk)
        }, status=204)
    
# class SinglePostView(RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer