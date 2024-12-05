from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=50, unique=True)
    count = models.IntegerField(default=0)

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateTimeField()
    topics = models.ManyToManyField(Topic, null=True)

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateTimeField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)