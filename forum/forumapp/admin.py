from django.contrib import admin
from forumapp import models

# Register your models here.

admin.site.register(models.Post)
admin.site.register(models.Comment)
admin.site.register(models.Topic)