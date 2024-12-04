from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateTimeField()

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateTimeField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)