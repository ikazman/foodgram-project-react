from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Favorite, Ingredient, IngredientsAmount, Recipe,
                            ShoppingCart, Tag)
from rest_framework import serializers
from users.serializers import UserSerializer


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = serializers.ReadOnlyField(source='ingredient.name')
    amount = serializers.IntegerField()
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientsAmount
        fields = ('id', 'name', 'amount', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(source='recipes_amount',
                                             many=True)
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
                and ShoppingCart.objects.filter(recipe=obj,
                                                user=request.user).exists())

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (request.user.is_authenticated
                and Favorite.objects.filter(recipe=obj,
                                            user=request.user).exists())

    def populate_amount(self, ingredients, recipe):
        for item in ingredients:
            id = item['ingredient']['id']
            ingredient = get_object_or_404(Ingredient, id=id)
            amount = item['amount']
            IngredientsAmount.objects.create(
                ingredient=ingredient,
                recipe=recipe,
                amount=amount)

    def create(self, data):
        ingredients = data.pop('recipes_amount')
        tags_in = data.pop('tags')
        recipe = Recipe.objects.create(**data)
        for tag in tags_in:
            recipe.tags.add(tag)
        self.populate_amount(ingredients, recipe)
        return recipe

    def update(self, data):
        ingredients = data.pop('recipes_amount')
        tags_in = data.pop('tags')
        recipe = super().update(recipe, data)
        recipe.tags.clear()
        for tag in tags_in:
            recipe.tags.add(tag)
        recipe.ingredients.clear()
        self.populate_amount(ingredients, recipe)
        return recipe


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = Base64ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = Base64ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time')
