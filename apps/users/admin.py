from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin, ImportExportModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'branch', 'is_superuser', 'is_staff', 'is_active',)
    list_filter = ('branch', 'is_superuser', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'phone', 'branch', 'password', 'is_superuser')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'phone', 'branch', 'password1', 'password2', 'is_superuser', 'is_staff',
                'is_active')}
         ),
    )
    search_fields = ('email', 'phone')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)

