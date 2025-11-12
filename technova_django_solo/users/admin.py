from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, VerificationToken

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_email_verified', 'date_joined')
    list_filter = ('is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    def is_email_verified(self, obj):
        return obj.is_active
    is_email_verified.boolean = True
    is_email_verified.short_description = 'Email Verificado'
    
    fieldsets = (
        (None, {
            'fields': ('username', 'password'),
        }),
        (_('Información Personal'), {
            'fields': ('first_name', 'last_name', 'email'),
        }),
        (_('Permisos'), {
            'fields': ('is_active', 'groups', 'user_permissions'),
        }),
    )
    
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    
    def get_inline_instances(self, request, obj):
        if not request.user.is_superuser:
            return []
        return super().get_inline_instances(request, obj)

@admin.register(VerificationToken)
class VerificationTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at', 'expires_at', 'is_valid')
    list_filter = ('created_at', 'expires_at')
    search_fields = ('user__username', 'user__email', 'token')
    ordering = ('-created_at',)
    
    readonly_fields = ('token', 'created_at', 'expires_at')
    
    def is_valid(self, obj):
        return obj.is_valid()
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
