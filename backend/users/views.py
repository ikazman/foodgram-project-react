from rest_framework import filters,status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import  AllowAny, IsAuthenticated


from .models import Follow, User
from .serializers import FollowSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter]
    search_fields = ['id', ]

    @action(detail=True,
            permission_classes=[AllowAny],
            methods=['delete', 'get'],
            url_path='subscribe')
    def subscribe(self, request):
        author = self.get_object()
        if request.method == 'GET':
            instance = Follow.objects.create(user=request.user, author=author)
            serializer = FollowSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            Follow.objects.filter(user=request.user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return None


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)
