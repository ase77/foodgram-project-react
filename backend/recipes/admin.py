from django.contrib import admin

from foodgram.settings import VALUE_DISPLAY
from .models import (
    Tag, Ingredient, Recipe, IngredientRecipe, Favorite, ShoppingCart
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name',)
    empty_value_display = VALUE_DISPLAY


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('measurement_unit',)
    empty_value_display = VALUE_DISPLAY


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author')
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name',)
    empty_value_display = VALUE_DISPLAY

    # def amount_tags(self, obj):
    #     print(f'FOOBAR___{obj}')
    #     print(f'FOOBAR___{obj.tags}')
    #     print(f'FOOBAR___{obj.tags.values_list('name')}')
    #     return obj

    # def amount_ingredients(self, obj):
    #     return "\n".join([i[0] for i in obj.ingredients.values_list('name')])


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    empty_value_display = VALUE_DISPLAY


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = VALUE_DISPLAY


@admin.register(ShoppingCart)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = VALUE_DISPLAY
