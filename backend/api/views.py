from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions, viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from users.models import CustomUser
from recipes.models import Tag, Ingredient, Recipe
from .serializers import CustomUserSerializer, SetPasswordSerializer, TagSerializer, IngredientSerializer, RecipeCreateSerializer, RecipeViewSerializer


class UserModelViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
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
             status=status.HTTP_401_UNAUTHORIZED)

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
        if serializer.is_valid():
            if not user.check_password(serializer.data.get("current_password")):
                return Response({'status': 'Текущий пароль не действителен'},
                            status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'status': 'Пароль успешно изменен'},
                            status=status.HTTP_204_NO_CONTENT)


class TagViewSet(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [permissions.AllowAny]
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = RecipeFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeViewSerializer
        return RecipeCreateSerializer

    def create(self, request, *args, **kwargs):
        if bool(request.user and request.user.is_authenticated):
            print(data.recipe.id)
            data = {'user': request.user.id, 'recipe': request.recipe.id}
            serializer = self.get_serializer(data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(
            {'status': 'Пользователь не авторизован'},
             status=status.HTTP_401_UNAUTHORIZED)

    def perform_create(self, serializer):
        serializer.save()

    # @staticmethod
    # def delete_method_for_actions(request, pk, model):
    #     user = request.user
    #     recipe = get_object_or_404(Recipe, id=pk)
    #     model_obj = get_object_or_404(model, user=user, recipe=recipe)
    #     model_obj.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    def destroy(self, request, *args, **kwargs):
        print(request.user)
        print(request.recipe.author)
        if bool(request.user == request.recipe.author):
            instance = get_object_or_404(Recipe, request.recipe.id)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'status': 'Недостаточно прав для удаления'},
             status=status.HTTP_403_FORBIDDEN)

    def perform_destroy(self, instance):
        instance.delete()
