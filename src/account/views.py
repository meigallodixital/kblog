from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import UserSerializer, ChangePasswordSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission


User = get_user_model()

class IsUser(BasePermission):

    message = 'Only can change your password'

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id

class UserCreate(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class UserInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsUser)
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()
