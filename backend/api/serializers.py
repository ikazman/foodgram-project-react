from django.core import exceptions
from rest_framework import serializers

from recipes.models import Ingredient, Tag, Recipe, Amount, FavoriteRecipies


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'color', 'slug',)


class RecipeSerializer(serializers.ModelSerializer):
    pass