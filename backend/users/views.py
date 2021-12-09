from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Follow, User
from .serializers import FollowSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @action(detail=True,
            permission_classes=[IsAuthenticated],
            methods=['delete', 'get'],
            url_path='subscribe')
    def subscribe(self, request, pk=None):
        author = self.get_object()
        if request.method == 'GET':
            if Follow.objects.filter(user=request.user,
                                     author=author).exists():
                return Response({'errors': 'Подписка уже создана'},
                                status=status.HTTP_400_BAD_REQUEST)
            Follow.objects.create(user=request.user, following=author)
            serializer = FollowSerializer(author, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            Follow.objects.filter(user=request.user, following=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)
