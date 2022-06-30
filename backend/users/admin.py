from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


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


admin.site.register(CustomUser, CustomUserAdmin)
