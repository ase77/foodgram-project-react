from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework.routers import DefaultRouter

from .views import UserModelViewSet, MeView

router_v1 = DefaultRouter()

router_v1.register(r'users', UserModelViewSet, basename='users')
# router_v1.register(r'users/me', MeView, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
    # path('users/me/', MeView.as_view()),
    path('auth/token/login/', TokenCreateView.as_view()),
    path('auth/token/logout/', TokenDestroyView.as_view()),
]
