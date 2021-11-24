from django.db import models

from users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField()
    image = models.ImageField()
    text = models.TextField()
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient',
                                         through='IngredientAmount')
    cooking_time = models.PositiveSmallIntegerField()


class Tag(models.Model):
    name = models.CharField()
    color = models.CharField()
    slug = models.SlugField()


class Ingredient(models.Model):
    name = models.CharField()
    measurement_unit = models.CharField()


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
