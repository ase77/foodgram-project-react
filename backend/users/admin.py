from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from foodgram.settings import VALUE_DISPLAY
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Follow


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        'id',
        'email',
        'username',
        'first_name',
        'last_name',
        'is_superuser'
    )
    list_filter = ('email', 'username')
    fieldsets = (
        (None, {'fields': (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'username',
                'first_name',
                'last_name',
                'password1',
                'password2',
                'is_superuser'
            )}
        ),
    )
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('id', 'username')
    empty_value_display = VALUE_DISPLAY


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')
    empty_value_display = VALUE_DISPLAY
