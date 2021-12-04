from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from recipes.models import (Favorite, Ingredient, IngredientsAmount, Recipe,
                            ShoppingCart, Tag)

from . import serializers
from .filters import IngredientFilter, RecipeFilter
from .permissions import IsAuthorOrReadOnly

User = get_user_model()

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-id')
    serializer_class = serializers.RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly, ]
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True,
            methods=['get', 'delete'],
            permission_classes=[IsAuthenticated, ],
            url_path='shopping_cart')
    def shopping_cart(self, request, pk=None):
        recipe = self.get_object()
        if request.method == 'GET':
            instance = ShoppingCart.objects.create(recipe=recipe,
                                                   user=request.user)
            serializer = serializers.ShoppingCartSerializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            ShoppingCart.objects.filter(recipe=recipe,
            user=request.user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return None

    @action(methods=['get'],
            detail=False,
            permission_classes=(IsAuthenticated,),
            url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        download_dict = {}
        ingredients = IngredientsAmount.objects.filter(
            recipe__cart__user=request.user).values_list(
                'ingredient__name',
                'ingredient__measurement_unit',
                'amount')
        for recipe in ingredients:
            name, units, amount = recipe
            if name in download_dict:
                new_amount = download_dict[name][0] + amount
                download_dict[name] = (new_amount, units)
            else:
                download_dict[name] = (amount, units)
        response = HttpResponse(content_type='.txt')
        response.write('\n'.join(f'{name} - {value[0]} {value[1]}'
                       for name, value in download_dict.items()))
        return response

    @action(detail=True,
            methods=['get', 'delete'],
            permission_classes=[IsAuthenticated, ],
            url_path='favorite')
    def favorite(self, request, pk=None):
        recipe = self.get_object()
        if request.method == 'GET':
            instance = Favorite.objects.create(recipe=recipe,
                                               user=request.user)
            serializer = serializers.FavoriteSerializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            Favorite.objects.filter(recipe=recipe, user=request.user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return None
