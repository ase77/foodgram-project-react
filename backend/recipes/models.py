from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models

from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField('Нименование', max_length=150, unique=True)
    color = ColorField('Цвет "HEX"', default="#e26c2d", unique=True)
    slug = models.SlugField('Слаг', max_length=20, unique=True)

    class Meta:
        verbose_name_plural = 'Тег'
        verbose_name = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Нименование', max_length=150)
    measurement_unit = models.CharField('ед.изм.', max_length=50)

    class Meta:
        verbose_name_plural = 'Ингредиент'
        verbose_name = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField('Название', max_length=200)
    text = models.CharField('Описание', max_length=200)
    cooking_time = models.IntegerField(
        validators=(
            MinValueValidator(1, 'минимальное время 1 мин.'),
        ),
        verbose_name='Время приготовления',
    )
    image = models.ImageField('Картинка', upload_to='recipes/')
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        related_name='recipes'
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name_plural = 'Рецепт'
        verbose_name = 'Рецепты'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_recipes',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients_recipes',
    )
    amount = models.IntegerField(
        validators=(
            MinValueValidator(1, 'минимальное количество 1'),
        ),
        verbose_name='Количество',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_ingredient'
            ),
        ]
        verbose_name = 'Ингредиент к рецепту'
        verbose_name_plural = 'Ингредиенты к рецептам'

    def __str__(self):
        return f'{self.recipe} - {self.amount}{self.ingredient}'


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorite_user',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='Рецепт',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite'
            ),
        ]
        verbose_name_plural = 'Избранные'
        verbose_name = 'Избранное'

    def __str__(self):
        return self.user.username


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='shopping_user',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_recipe',
        verbose_name='Рецепт',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart'
            ),
        ]
        verbose_name_plural = 'Списки покупок'
        verbose_name = 'Список покупок'

    def __str__(self):
        return self.user.username
