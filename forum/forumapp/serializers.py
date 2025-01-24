from rest_framework import serializers
from .models import User, Topic, Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'content', 'author', 'date', 'topics')
    # title = serializers.CharField(max_length=120)
    # content = serializers.CharField()
    # author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # date = serializers.DateTimeField()
    # topics = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all(), many=True)

    def create(self, validated_data):
        return Post.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.author = validated_data.get('author', instance.author)
        instance.date = validated_data.get('date', instance.date)
        instance.topics = validated_data.get('topics', instance.topics)

        instance.save()
        return instance