from django.urls import path
from .views import PostView

urlpatterns = [
    path('posts/', PostView.as_view()),
    path('posts/<int:pk>', PostView.as_view())
]