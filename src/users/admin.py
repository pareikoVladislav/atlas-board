from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from src.users.models import User


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    model = User

    list_display = [
        'email',
        'first_name',
        'last_name',
        'position',
        'is_active',
        'is_staff',
        'date_joined'
    ]
    list_filter = [
        'is_active',
        'is_staff',
        'is_superuser',
        'position',
        'date_joined'
    ]
    search_fields = [
        'email',
        'first_name',
        'last_name'
    ]
    ordering = ['email']

    fieldsets = (
        (
            None, {
            "fields": ('password', 'email')
        }
         ),
        (
            _("Personal info"), {
            "fields": ('first_name', 'last_name', 'position')
        }
         ),
        (
            _("Permissions"), {
            "fields": ('is_superuser', 'groups', 'user_permissions', 'is_active', 'is_staff')
        }
         ),
        (
            _("Important dates"), {
                "fields": ('last_login', 'date_joined')
            }
        )
    )

    readonly_fields = ('last_login', 'date_joined')

    add_fieldsets = (
        (
            None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'position')
            }
         ),
    )

admin.site.unregister(Group)
admin.site.register(Group)
