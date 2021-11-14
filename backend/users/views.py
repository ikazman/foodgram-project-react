from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdmin
from .serializers import RegisterSerializer, TokenSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin, ]
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]

    @action(detail=False,
            permission_classes=[IsAuthenticated],
            methods=['patch', 'get'])
    def me(self, request):
        serializer = self.get_serializer(self.request.user)
        if request.method == 'PATCH':
            user = get_object_or_404(User, username=self.request.user)
            serializer = self.get_serializer(user,
                                             data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignupViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['POST'])
    def signup(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        first_name = serializer.validated_data.get('first_name')
        last_name = serializer.validated_data.get('last_name')
        password = serializer.validated_data.get('password')

        User.objects.get_or_create(username=username,
                                   email=email,
                                   first_name=first_name,
                                   last_name=last_name,
                                   password=password)

        return Response({'email': email,
                         'username': username,
                         'first_name': first_name,
                         'last_name': last_name,
                         'password': password},
                        status=status.HTTP_200_OK)


class TokenViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['post'])
    def token(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password')
        email = serializer.validated_data.get('email')
        user = get_object_or_404(User, email=email, password=password)
        if default_token_generator.check_token(user, email):
            refresh_token = RefreshToken.for_user(user)
            return Response({'token': str(refresh_token.access_token)})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
