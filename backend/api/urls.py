from django.urls import include, path
from rest_framework.routers import DefaultRouter
from djoser.views import TokenDestroyView, TokenCreateView

from .views import UserModelViewSet

router_v1 = DefaultRouter()

router_v1.register(r'users', UserModelViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/token/login/', TokenCreateView.as_view()),
    path('auth/token/logout/', TokenDestroyView.as_view()),
]
