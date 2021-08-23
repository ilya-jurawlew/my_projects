from django.contrib.auth import authenticate, login
from rest_framework import generics, status

from app_users.models import Profile
from drf_users.serializers import RegisterSerializer, UserSerializer, UserSmallSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class ListUsersAPI(generics.ListAPIView):
    """Список всех пользователей"""
    queryset = Profile.objects.all()
    serializer_class = UserSmallSerializer
    permission_classes = (AllowAny, )


class DetailUserAPI(generics.RetrieveAPIView):
    """Список всех пользователей"""
    queryset = Profile.objects.filter()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )


class RegisterUserAPI(generics.GenericAPIView):
    """Регистрация пользователя"""
    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.data}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(TokenObtainPairView):
    """Аутентификация пользователя"""
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return Response(status=status.HTTP_200_OK)
