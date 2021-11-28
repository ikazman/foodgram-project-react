from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Follow, User
from .serializers import FollowSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny, ]
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter]
    search_fields = ['id', ]

    @action(detail=True,
            permission_classes=[permissions.IsAuthenticated],
            methods=['delete', 'get'],
            url_path='subscribe')
    def subscribe(self, request):
        author = self.get_object()
        if request.method == 'GET':
            Follow.objects.create(user=request.user, following=author)
            serializer = FollowSerializer(author,
                                          context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        Follow.objects.filter(user=request.user, following=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)
