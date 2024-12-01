# serializers/user_activity_serilaizers.py
from rest_framework import serializers
from testapp.models.user_activity import UserActivity

class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ['id', 'full_name', 'email', 'action_performed', 'action_type', 'timestamp', 'role_name', 'ip_address', 'user']
