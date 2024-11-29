from testapp.models.user_activity import UserActivity
from rest_framework import serializers

class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = '__all__'
        
