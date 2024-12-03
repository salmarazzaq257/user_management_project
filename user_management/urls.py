from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from testapp.views.auth import UserLoginView, ResetPasswordWithTokenView,GenerateResetTokenView

from django.urls import path
from testapp.views.custom_user import (
    CreateUserView,
    ListUsersView,
    UpdateUserView,
    ActivationView,
    DeleteUserView,
   
)
from testapp.views.role_management import RoleManagementiew, UpdateRoleView, ListRolesView
from testapp.views.user_activity import LogActivityView
from testapp.views.role_permissions import RolePermissionsView


urlpatterns = [
    path('admin/', admin.site.urls),
    # User Management URLs
    path('users/', CreateUserView.as_view(), name='create_user'),
    path('users/list', ListUsersView.as_view(), name='list-users'),
    path('users/<int:id>/', UpdateUserView.as_view(), name='update_user'),
    path('users/<int:id>/ActivationView/', ActivationView.as_view(), name='activate-deactivate-user'),
    path('users/delete/<int:id>/', DeleteUserView.as_view(), name='delete_user'),
    # Authentication URLs
    
    path('auth/login/', UserLoginView.as_view(), name='user_login'),
    path('auth/generate-reset-token/', GenerateResetTokenView.as_view(), name='generate_reset_token'),
    path('auth/reset-password/', ResetPasswordWithTokenView.as_view(), name='reset_password'),
    # Role Management URLs
    path('roles/', RoleManagementiew.as_view(), name='create_role'),
    path('roles/<int:id>/', UpdateRoleView.as_view(), name='update_role'),
    path('roles/list/', ListRolesView.as_view(), name='list_roles'),
    path('role-permissions/', RolePermissionsView.as_view(), name='assign_permissions'),
    # User Activity URLs
    path('activities/', LogActivityView.as_view(), name='activities_list'),  # GET and POST for activity logs
    path('activities/export/', LogActivityView.as_view(), name='activities_export_list'),  # Export CSV endpoint

    # DRF URLs
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # Include DRF URLs
    
   
]

