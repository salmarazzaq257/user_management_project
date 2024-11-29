from testapp.models.role_management import RoleManagement
from rest_framework import serializers

class RoleManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleManagement
        fields = '__all__'
