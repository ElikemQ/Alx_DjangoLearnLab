from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'birthdate', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'birthdate', 'profile_picture', 'is_staff', 'is_active'),
        }),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'birthdate', 'is_staff', 'is_active')

    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    search_fields = ('username', 'email')

    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)

