from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions, viewsets, views, status
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'username'
    pagination_class = PageNumberPagination


# class MeView(views.APIView):
#     permission_classes = (permissions.IsAuthenticated,)

#     def get(self, request):
#         serializer = CustomUserSerializer(request.user)
#         return Response(serializer.data)
