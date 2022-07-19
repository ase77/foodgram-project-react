from django_filters.rest_framework import FilterSet, filters
from recipes.models import Recipe


class RecipeFilter(FilterSet):
    author = filters.AllValuesFilter(field_name='author__id')
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorite_user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shopping_user=self.request.user)
        return queryset


# class RecipeFilter(FilterSet):
#     author = filters.AllValuesFilter(field_name='author__id')
#     tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
#     is_favorited = filters.BooleanFilter(method='filter_queryset')
#     is_in_shopping_cart = filters.BooleanFilter(method='filter_queryset')

#     class Meta:
#         model = Recipe
#         fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']

#     def filter_queryset(self, queryset):
#         data = self.form.cleaned_data
#         user = self.request.user
#         if data['is_favorited']:
#             return queryset.filter(favorite_recipe__user=user)
#         elif data['is_in_shopping_cart']:
#             return queryset.filter(shopping_recipe__user=user)
#         elif data['author']:
#             return queryset.filter(author__id=user.id)
#         elif data['tags']:
#             data_tag = list(data['tags'])
#             for value in data_tag:
#                 qs = queryset.filter(tags__slug=value)
#             return qs
#         return queryset
