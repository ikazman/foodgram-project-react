import django_filters.rest_framework as django_filters
from django_filters.rest_framework import FilterSet

from recipes.models import Ingredient, Recipe


class IngredientFilter(FilterSet):
    name = django_filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = Ingredient
        fields = ('name', )


class RecipeFilter(FilterSet):
    tags = django_filters.CharFilter(field_name='tags', lookup_expr='exact')
    author = django_filters.CharFilter(field_name='author', lookup_expr='exact')
    is_in_favorited = django_filters.BooleanFilter(
        method='filter_is_favorited')
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='filter_is_in_shopping_cart')

    def filter_is_favorited(self, queryset, value):
        if value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, value):
        if value:
            return queryset.filter(cart__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)
