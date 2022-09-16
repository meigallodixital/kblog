from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'body', 'created_at',
                  'updated_at', 'image', 'author', 'slug']
        read_only_fields = ['author']
        lookup_field = 'slug'


class PostCreateSerializer(PostSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta(PostSerializer.Meta):
        fields = ['title', 'body', 'published_at', 'image', 'author', 'slug']
        read_only_fields = ['author', 'slug']


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'body', 'created_at', 'updated_at',
                  'published_at', 'image', 'author', 'slug']
