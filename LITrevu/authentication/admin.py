
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission
from .models import User

class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role', 'follows')}),
    )
    list_display = ('username', 'email', 'role')
    list_filter = ('role',)

admin.site.register(User, UserAdmin)
admin.site.register(Permission)
