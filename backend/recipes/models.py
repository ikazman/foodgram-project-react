from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Ингредиент')
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиент'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тега',
        max_length=200, unique=True
    )
    color = models.CharField(
        verbose_name='Цветовой HEX-код',
        unique=True)
    slug = models.SlugField(
        max_length=50,
        unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.SET_NULL,
        related_name='recipes',
        null=True,
        blank=True)

    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200
    )

    image = models.ImageField(
        verbose_name='Изображение блюда',
        upload_to='images/',
        null=True,
        blank=True)

    text = models.TextField(verbose_name='Описание рецепта')

    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        through='Amount',
        related_name='ingredients'
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='tags',

    )

    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)',
        null=True,
        validators=[MinValueValidator(1)])

    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Amount(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return self.amount


class FavoriteRecipies(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_pair'),
        ]

    def __str__(self):
        return f'Избранные рецепты: {self.recipe.name}'

