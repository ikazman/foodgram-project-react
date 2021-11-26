from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)
from rest_framework import serializers
from users.models import Follow, User
from users.serializers import UserSerializer


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientAmountSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):

    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'author',
            'ingredients',
            'image',
            'text',
            'cooking_time',
            'tags',
            'is_in_shopping_cart',
            'is_favorited',
        )

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (request.user.is_authenticated
                and obj.filter(user=request.user).exists())

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (request.user.is_authenticated
                and obj.filter(user=request.user).exists())


class RecipeFollowSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(queryset=Recipe.objects.all(),
                                        slug_field='name')
    image = Base64ImageField(read_only=True)
    cooking_time = serializers.SlugRelatedField(queryset=Recipe.objects.all(),
                                                slug_field='cooking_time')

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe


class ShoppingCartSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    name = serializers.SlugRelatedField(queryset=Recipe.objects.all(),
                                        slug_field='name')
    image = Base64ImageField(read_only=True)
    cooking_time = serializers.SlugRelatedField(queryset=Recipe.objects.all(),
                                                slug_field='cooking_time')

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    name = serializers.SlugRelatedField(queryset=Recipe.objects.all(),
                                        slug_field='name')
    image = Base64ImageField(read_only=True)
    cooking_time = serializers.SlugRelatedField(queryset=Recipe.objects.all(),
                                                slug_field='cooking_time')

    class Meta:
        model = Favorite
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
        return obj.filter(user=request.user).exists()

    def get_recipes(self, obj):
        request=self.context.get('request')
        recipes_limit=int(self.context.get('recipes_limit'))
        if recipes_limit:
            recipes=obj.recipes.all()[:recipes_limit]
        else:
            recipes=obj.recipes.all()
        serializer=RecipeFollowSerializer(recipes, many = True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
