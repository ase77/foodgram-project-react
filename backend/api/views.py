from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)
from rest_framework import filters, permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from users.models import CustomUser, Follow

from .custom_viewset import (CreateListRetrieveViewSet, ListRetrieveViewSet,
                             RetrieveListCreateUpdateDestroyViewSet)
from .download_shopping_cart import download_pdf
from .filters import RecipeFilter
from .serializers import (CustomUserSerializer, FavoriteSerializer,
                          FollowSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeViewSerializer,
                          SetPasswordSerializer, ShoppingCartSerializer,
                          TagSerializer)


class UserModelViewSet(CreateListRetrieveViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = PageNumberPagination

    def retrieve(self, request, *args, **kwargs):
        if bool(request.user and request.user.is_authenticated):
            pk = kwargs.get('pk')
            instance = get_object_or_404(CustomUser, pk=pk)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response(
            {'status': 'Пользователь не авторизован'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    @action(methods=['get'], detail=False,
            permission_classes=[permissions.IsAuthenticated], url_name='users')
    def me(self, request, *args, **kwargs):
        self.object = get_object_or_404(CustomUser, pk=request.user.id)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)

    @action(methods=['post'], detail=False,
            permission_classes=[permissions.IsAuthenticated], url_name='users')
    def set_password(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, pk=request.user.id)
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not user.check_password(
                serializer.data.get("current_password")):
            return Response(
                {'status': 'Текущий пароль не действителен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response(
            {'status': 'Пароль успешно изменен'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(methods=['get'], detail=False,
            permission_classes=[permissions.IsAuthenticated],
            url_name='users')
    def subscriptions(self, request, *args, **kwargs):
        user = request.user
        print(f'FOOBAR_user_!_{user}')
        queryset = CustomUser.objects.filter(following__user=user)
        serializer = FollowSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True,
            permission_classes=[permissions.IsAuthenticated],
            url_name='users')
    def subscribe(self, request, *args, **kwargs):
        author_id = kwargs.get('pk', None)
        user = request.user
        author = get_object_or_404(CustomUser, id=author_id)
        if author == user:
            return Response(
                {'status': 'Нельзя подписаться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif Follow.objects.filter(user=user, author_id=author_id).exists():
            return Response(
                {'status': f'На автора "{author}" вы уже подписаны'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            Follow.objects.create(user=user, author_id=author_id)
            return Response(FollowSerializer(
                author,
                context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )

    @subscribe.mapping.delete
    def delete_subscribe(self, request, *args, **kwargs):
        author_id = kwargs.get('pk', None)
        user = request.user
        author = get_object_or_404(CustomUser, id=author_id)
        if Follow.objects.filter(user=user, author_id=author_id).exists():
            follow = get_object_or_404(Follow, user=user, author_id=author_id)
            follow.delete()
            return Response(
                {'status': f'Вы успешно отписались от автора "{author}"'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {'status': f'Вы не подписаны на автора "{author}"'},
            status=status.HTTP_400_BAD_REQUEST
        )


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']


class RecipeViewSet(RetrieveListCreateUpdateDestroyViewSet):
    queryset = Recipe.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeViewSerializer
        return RecipeCreateSerializer

    def create(self, request, *args, **kwargs):
        if bool(request.user and request.user.is_authenticated):
            serializer = self.get_serializer(
                data=request.data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        return Response(
            {'status': 'Пользователь не авторизован'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        recipe = get_object_or_404(Recipe, id=pk)
        if bool(request.user == recipe.author):
            self.perform_destroy(recipe)
            return Response(
                {'status': 'Рецепт успешно удалён'},
                status=status.HTTP_204_NO_CONTENT
            )
        elif bool(request.user and not request.user.is_authenticated):
            return Response(
                {'status': 'Пользователь не авторизован'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(
            {'status': 'Недостаточно прав для удаления'},
            status=status.HTTP_403_FORBIDDEN
        )

    def perform_destroy(self, recipe):
        recipe.delete()

    def update(self, *args, **kwargs):
        return Response(
            {'status': 'Method "PUT" not allowed.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        pk = kwargs.get('pk', None)
        instance = get_object_or_404(Recipe, id=pk)
        if bool(request.user == instance.author):
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        elif bool(request.user and not request.user.is_authenticated):
            return Response(
                {'status': 'Пользователь не авторизован'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(
            {'status': 'Недостаточно прав для обновления'},
            status=status.HTTP_403_FORBIDDEN
        )

    def perform_update(self, serializer):
        serializer.save()

    @action(methods=['post'], detail=True,
            permission_classes=[permissions.IsAuthenticated],
            url_name='recipes')
    def favorite(self, request, *args, **kwargs):
        recipe_pk = kwargs.get('pk', None)
        user_id = request.user.id
        if Favorite.objects.filter(
                user=request.user, recipe=recipe_pk).exists():
            return Response(
                {'status': 'Рецепт уже был добавлен в избранное'},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {'user': user_id, 'recipe': recipe_pk}
        serializer = FavoriteSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, *args, **kwargs):
        recipe_pk = kwargs.get('pk', None)
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_pk)
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
            favorite.delete()
            return Response(
                {'status': f'Рецепт "{recipe.name}" удален из избранного'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {'status': f'Рецепт "{recipe.name}" не находится в избранном'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(methods=['post'], detail=True,
            permission_classes=[permissions.IsAuthenticated],
            url_name='recipes')
    def shopping_cart(self, request, *args, **kwargs):
        recipe_pk = kwargs.get('pk', None)
        user_id = request.user.id
        if ShoppingCart.objects.filter(
                user=request.user, recipe=recipe_pk).exists():
            return Response(
                {'status': 'Рецепт уже был добавлен в список покупок'},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {'user': user_id, 'recipe': recipe_pk}
        serializer = ShoppingCartSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, *args, **kwargs):
        recipe_pk = kwargs.get('pk', None)
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_pk)
        if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
            favorite = get_object_or_404(
                ShoppingCart, user=user, recipe=recipe
            )
            favorite.delete()
            return Response(
                {'status': f'Рецепт "{recipe.name}" удален из списка покупок'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {'status': f'Рецепта "{recipe.name}" ещё нет в списке покупок'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(methods=['get'], detail=False,
            permission_classes=[permissions.IsAuthenticated],
            url_name='recipes')
    def download_shopping_cart(self, request, *args, **kwargs):
        ingredients = IngredientRecipe.objects.filter(
            recipe__shopping_recipe__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount'
        )
        if not ingredients:
            return Response(
                {'status': 'Нет рецептов в списке покупок'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return download_pdf(ingredients)
