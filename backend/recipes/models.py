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

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['color', 'name'], name='unique_tag_pair')]
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Название ингредиента',
                            max_length=200)
    measurement_unit = models.CharField(verbose_name='Единица измерения',
                                        max_length=150)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['name', 'measurement_unit'], name='unique_unit_pair')]
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор рецепта',
                               related_name='recipes')
    name = models.CharField(verbose_name='Название рецепта', max_length=200)
    image = models.ImageField(verbose_name='Изображение рецепта',
                              upload_to='recipe_image/')
    text = models.TextField(verbose_name='Описание рецепта')
    tags = models.ManyToManyField(Tag, related_name='recipes',
                                  verbose_name='Теги')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsAmount',
        through_fields=('recipe', 'ingredient'),
        related_name='recipes',
        verbose_name='Ингредиенты')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['author', 'name'], name='unique_recipe_pair')]
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientsAmount(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name='ingredient_amount',
                                   verbose_name='Ингредиент')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='recipes_amount',
                               verbose_name='Рецепт')
    amount = models.PositiveSmallIntegerField(verbose_name='Количество')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['ingredient', 'recipe'], name='unique_ingredient_pair')]
        verbose_name = 'Количество ингредиентов'


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='cart',
                               verbose_name='Рецепт')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='cart')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['recipe', 'user'], name='unique_cart_pair')]
        verbose_name = 'Список покупок'


class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favorites_recipe',
                               verbose_name='Рецепт')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorites_user')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['recipe', 'user'], name='unique_favorite_pair')]
