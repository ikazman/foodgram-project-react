from django.contrib import admin
from recipes.models import IngredientsAmount


class IngredientAmountInline(admin.TabularInline):
    model = IngredientsAmount
