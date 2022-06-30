from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserModelViewSet, ObtainToken

router_v1 = DefaultRouter()

router_v1.register(r'users', UserModelViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/token/login/', ObtainToken.as_view()),
]
