from django.db.models import constraints
from colorfield.fields import ColorField

from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(verbose_name='Название тега',
                            unique=True, max_length=200)
    color = ColorField(default='#FF0000')
    slug = models.SlugField(verbose_name='Идентификатор тега', unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Название ингредиента', max_length=200)
    measurement_unit = models.CharField('Название ингредиента',
                                        max_length=150)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор рецепта',
                               related_name='recipes')
    name = models.CharField(verbose_name='Название рецепта', max_length=200)
    image = models.ImageField(verbose_name='Изображение рецепта',
                              upload_to='recipe_image/')
    text = models.TextField(verbose_name='Описание рецепта')
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsAmount',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления')


class IngredientsAmount(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name='recipes_amount',
                                   verbose_name='Ингредиент')
    recipe = models.ForeignKey(Recipe, related_name='recipes_amount',
                               verbose_name='Рецепт')
    amount = models.PositiveSmallIntegerField(verbose_name='Количество')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['ingredient', 'recipe'], name='unique_ingredient_pair')]


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='recipes_in_cart',
                               verbose_name='Рецепт')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='users_cart')


class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favorite_recipe',
                               verbose_name='Рецепт')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorite_user')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['recipe', 'user'], name='unique_favorite_pair')]
