from rest_framework import serializers
from .models import User, Topic, Post

class PostSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    date = serializers.DateTimeField()
    topics = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all(), many=True)

    def create(self, validated_data):
        return Post.objects.create(**validated_data)