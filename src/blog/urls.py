from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView

app_name = 'blog'

urlpatterns = [
	path('', PostListView.as_view(), name='post-list'),
	path('new/', PostCreateView.as_view(), name='post-create'),
	path('read/<str:slug>/', PostDetailView.as_view(), name='post-view-update-delete')
]