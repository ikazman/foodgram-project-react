from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (Favorite, Ingredient, IngredientsAmount, Recipe,
                            ShoppingCart, Tag)
from users.serializers import UserSerializer


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientAmountSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
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
    tags = TagSerializer(read_only=True, many=True)
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

    def create_amount(self, ingredients, recipe):
        for item in ingredients:
            id = item['ingredient']['id']
            amount = item['amount']
            IngredientsAmount.objects.create(
                ingredient=Ingredient(id=id),
                recipe=recipe,
                amount=amount)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipes_amount')
        recipe = Recipe.objects.create(**validated_data)
        tags_in = self.initial_data.get('tags')
        recipe.tags.set(tags_in)
        self.create_amount(ingredients_data, recipe)
        return recipe

    def update(self, recipe, validated_data):
        ingredients_data = validated_data.pop('recipes_amount')
        tags_in = self.initial_data.get('tags')
        recipe = super().update(recipe, validated_data)
        recipe.tags.clear()
        recipe.tags.set(tags_in)
        recipe.ingredients.clear()
        self.create_amount(ingredients_data, recipe)
        return recipe

    def validate_ingredients(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            return serializers.ValidationError(
                'В рецепте отсутствуют ингредиенты!')
        for item in ingredients:
            if int(item['amount']) < 1:
                return serializers.ValidationError(
                    'Количество ингридиента не может быть нулевым!')
        return data

    def validate_cooking_time(self, data):
        if data < 1:
            return serializers.ValidationError('Время меньше нуля!')
        return data


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
