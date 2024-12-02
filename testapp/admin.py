from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, RoleManagement, RolePermission, UserActivity

# Customize User Admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff','role', 'is_active', 'is_confirmed', 'login_count')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'is_confirmed', 'role')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'is_confirmed', 'login_count', 'current_login_ip', 'last_login_ip'),
        }),
    )

@admin.register(RoleManagement)
class RoleManagementAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'is_active')
    search_fields = ('role_name',)
    list_filter = ('is_active',)

@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'main_module', 'module_name', 'view_access', 'create_access', 'update_access', 'delete_access')
    search_fields = ('role__role_name', 'main_module', 'module_name')
    list_filter = ('main_module', 'module_name')


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_type', 'timestamp', 'role_name', 'ip_address')
    search_fields = ('user__email', 'action_type', 'role_name')
    list_filter = ('timestamp',)

