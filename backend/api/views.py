from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, IngredientsAmount, Recipe,
                            ShoppingCart, Tag)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers
from .permissions import IsAuthorOrStaffOrReadOnly


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    filter_backends = [DjangoFilterBackend, ]


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    filter_backends = [DjangoFilterBackend, ]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-id')
    serializer_class = serializers.RecipeSerializer
    permission_classes = [IsAuthorOrStaffOrReadOnly, ]
    filter_backends = [DjangoFilterBackend, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True,
            methods=['get', 'delete'],
            permission_classes=[IsAuthenticated, ],
            url_path='shopping_cart')
    def shopping_cart(self, request):
        recipe = self.get_object()
        if request.method == 'GET':
            cart = ShoppingCart.objects.create(recipe=recipe,
                                               user=request.user)
            serializer = serializers.ShoppingCartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        ShoppingCart.objects.filter(recipe=recipe, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'],
            detail=False,
            permission_classes=(IsAuthenticated,),
            url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        ingridients_to_buy = {}
        recipes_list = request.user.recipes_list.all()

        for recipe in recipes_list:
            ingredients = IngredientsAmount.objects.filter(
                recipe=recipe.recipe)
            for ingredient in ingredients:
                name = ingredients.name
                amount = ingredients.amount
                measurment = ingredient.measurement_unit
                if name not in ingridients_to_buy:
                    ingridients_to_buy[name] = {
                        'amount': amount,
                        'measurment': measurment
                    }
                ingridients_to_buy[recipe.recipe.name]['amount'] += amount
        buy_list = []
        for item in ingridients_to_buy:
            amount = ingridients_to_buy[item]['amount']
            units = ingridients_to_buy[item]['measurment']
            to_buy = f'{item} - {amount} {units}'
            buy_list.append(to_buy)
        response = HttpResponse(buy_list, content_type='plain/text')
        response['Content-Disposition'] = (f'attachment '
                                           f'filename="buy_list.txt"')
        return response

    @action(detail=True,
            methods=['get', 'delete'],
            permission_classes=[IsAuthenticated, ],
            url_path='favorite')
    def favorite(self, request):
        recipe = self.get_object()
        if request.method == 'get':
            favorited = Favorite.objects.create(recipe=recipe,
                                                user=request.user)
            serializer = serializers.FavoriteSerializer(favorited)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        Favorite.objects.filter(recipe=recipe, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
