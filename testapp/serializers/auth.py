from rest_framework import serializers
from django.contrib.auth import authenticate
from testapp.views.custom_user import CustomUser  # Assuming you are using a custom user model

class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    remember_me = serializers.BooleanField(required=False, default=False)  # Optional "Remember Me" field

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Ensure email and password are present
        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        # Authenticate user (This will check if user exists, is active, and validate password)
        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        # Check if the user is confirmed (if required)
        if not user.is_confirmed:
            raise serializers.ValidationError("Email is not confirmed.")
        
        # Returning validated data
        data['user'] = user  # Optionally, you can include the user object in the validated data
        return data
