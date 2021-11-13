from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('user',
                  'password',
                  'email',
                  'first_name',
                  'last_name',
                  'role',)


class RegisterSerializer(serializers.ModelSerializer):

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('"me" not allowed as username')
        return value

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)
