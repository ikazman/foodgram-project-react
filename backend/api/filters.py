from django_filters import FilterSet, filters

from django.contrib.auth import get_user_model

from recipes.models import Ingredient, Recipe

User = get_user_model()


class IngredientFilter(FilterSet):

    name = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):

    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(method='is_in_favorited')
    is_in_shopping_cart = filters.BooleanFilter(method='is_shopping_cart')

    def is_in_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorites_recipe__user=self.request.user)
        return queryset

    def is_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(cart__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('author',
                  'tags',
                  'is_favorited',
                  'is_in_shopping_cart',)
