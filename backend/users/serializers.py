from drf_extra_fields.fields import Base64ImageField
from recipes.models import Recipe
from rest_framework import serializers

from .models import Follow, User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (request.user.is_authenticated
                and Follow.objects.filter(author=obj,
                                          user=request.user).exists())

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class RecipeFollowSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    image = Base64ImageField(read_only=True)
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes_list = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes_list',
            'recipes_count')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return Follow.objects.filter(author=obj, user=request.user).exists()

    def get_recipes_list(self, obj):
        request = self.context.get('request')
        recipes_limit = int(self.context.get('recipes_limit'))
        if recipes_limit:
            recipes = obj.recipes.all()[:recipes_limit]
        else:
            recipes = obj.recipes.all()
        serializer = RecipeFollowSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
