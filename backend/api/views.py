from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions, viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from users.models import CustomUser
from .serializers import CustomUserSerializer, SetPasswordSerializer


class UserModelViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.AllowAny,)

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
                            status=status.HTTP_204_NO_CONTENT,)
