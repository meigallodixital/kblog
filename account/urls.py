from django.urls import path
from .views import UserInfo, UserCreate

app_name = 'user'

urlpatterns = [
	path('register/',UserCreate.as_view(), name="create_user"),
	path('getinfo/', UserInfo.as_view(), name="user_info"),
]
