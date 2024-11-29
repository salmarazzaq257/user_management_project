from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from testapp.views import custom_user ,role_management, role_permissions ,user_activity

# Swagger Schema Configuration
schema_view = get_schema_view(
    openapi.Info(
        title="User Management API",
        default_version="v1",
        description="API documentation for the User Management project.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@usermanagement.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticatedOrReadOnly],

)

from django.urls import path
from testapp.views.custom_user import (
    CreateUserView,
    UpdateUserView,
    DeleteUserView,
    UserLoginView,
    ResetPasswordView,
   
)
from testapp.views.role_management import CreateRoleView, UpdateRoleView, ListRolesView
from testapp.views.user_activity import LogActivityView, ActivityLogsView
from testapp.views.role_permissions import AssignPermissionsView



urlpatterns = [
    path('users/', CreateUserView.as_view(), name='create_user'),
    path('users/<int:id>/', UpdateUserView.as_view(), name='update_user'),
    path('users/delete/<int:id>/', DeleteUserView.as_view(), name='delete_user'),
    path('auth/login/', UserLoginView.as_view(), name='user_login'),
    path('auth/reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('roles/', CreateRoleView.as_view(), name='create_role'),
    path('roles/<int:id>/', UpdateRoleView.as_view(), name='update_role'),
    path('roles/list/', ListRolesView.as_view(), name='list_roles'),
    path('role-permissions/', AssignPermissionsView.as_view(), name='assign_permissions'),
    path('activities/', LogActivityView.as_view(), name='log_activity'),
    path('activities/logs/', ActivityLogsView.as_view(), name='activity_logs'),


    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # Include DRF URLs
    
    # Swagger Documentation
    path('swagger.<str:format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
