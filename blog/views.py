from django.utils.timezone import now
from django.views.generic.base import RedirectView
from rest_framework import filters
from rest_framework import generics
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticatedOrReadOnly,
    BasePermission,
    AllowAny
)
from .models import Post
from .serializers import PostSerializer, PostCreateSerializer, PostListSerializer


class IsAuthorOrReadOnly(BasePermission):

    message = 'Edit or delete posts is restricted to the author'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class PostHome(RedirectView):
    permanent = True
    query_string = True
    pattern_name = 'blog:post-list'


class PostListView(generics.ListAPIView):
    queryset = Post.objects.filter(published_at__lte=now())
    permission_classes = (AllowAny,)
    serializer_class = PostListSerializer
    ordering = ['-published_at']
    filterset_fields = ['published_at', 'title']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'body', 'author__username', 'author__email']
    ordering_fields = ['published_at', 'title']


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)
    serializer_class = PostCreateSerializer


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)
    serializer_class = PostSerializer
    lookup_field = 'slug'
