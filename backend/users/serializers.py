from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import Follow, User


class UserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None:
            return False
        if request.user.is_anonymous:
            return False
        else:
            return Follow.objects.filter(user=request.user,
                                         author=obj).exists()


class RegisterSerializer(UserCreateSerializer):

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('"me" not allowed as username')
        return value

    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'username',
                  'first_name',
                  'last_name',
                  'password',)
