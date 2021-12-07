from recipes.models import IngredientsAmount

from django.contrib import admin


class IngredientAmountInline(admin.TabularInline):
    model = IngredientsAmount
