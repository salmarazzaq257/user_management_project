from testapp.models.custom_user import CustomUser
from rest_framework import serializers
from testapp.serializers.role_serializers import RoleManagementSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    role = RoleManagementSerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['username', 'email','password','role']