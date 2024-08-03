"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from ..core import models


class UserAdmin(BaseUserAdmin):
    """Define admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'username']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
         ),
        ('Important dates', {'fields': ('last_login',)})
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'username',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )
    search_fields = ('email',)


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Brand)
