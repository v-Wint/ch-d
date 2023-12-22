from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    """Class to specify User modle on admin panel"""
    model = User
    list_display = ['username', 'email', 'is_moderator', 'is_staff', 'about', 'slug']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'is_moderator', 'is_staff', 'pfp', 'about')}),
    )
    add_fieldsets = (
        (None,
         {'fields': ('username', 'email', 'is_moderator', 'is_staff', 'pfp', 'about', 'slug')}
         ),
    )

admin.site.register(User, CustomUserAdmin)
