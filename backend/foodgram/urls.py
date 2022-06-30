from django.contrib import admin
from django.urls import include, path


api = [
    path('', include('users.urls')),
    # path('auth/', include('users.urls')),
    # path('recipes/', include('api.urls')),
]

urlpatterns = [
    path('api/', include(api)),
    path('admin/', admin.site.urls),
]
