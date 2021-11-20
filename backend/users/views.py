from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import RegisterSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter]
    search_fields = ['id', ]

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterSerializer
        return UserSerializer

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
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
