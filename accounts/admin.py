from django.contrib import admin

# Register your models here.
"""Integrate with admin module."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import CustomUser


# https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#a-full-example
# You are:
# Extending the original UserAdmin class that Django admin provides.
# Replacing the use of username for email.
# Registering your new class to be used by Django admin for your new User model.


@admin.register(CustomUser)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'dob',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','phone_number', 'dob', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'dob', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
