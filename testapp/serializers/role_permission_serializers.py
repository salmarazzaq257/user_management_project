from testapp.models.role_permission import RolePermission
from rest_framework import serializers

class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = '__all__'
        