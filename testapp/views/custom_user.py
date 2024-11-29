from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from testapp.models.custom_user import CustomUser
from testapp.serializers.user_serializers import CustomUserSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import uuid


class CreateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id, *args, **kwargs):
        user = CustomUser.objects.get(id=id)
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id, *args, **kwargs):
        user = CustomUser.objects.get(id=id)
        user.soft_delete()  # Using the soft delete method
        return Response({"detail": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class UserLoginView(APIView):

  class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(email=email, password=password)
        
        if user is not None:
            if user.deleted_at is not None:
                return Response({"error": "This user has been deleted."}, status=status.HTTP_400_BAD_REQUEST)
            
            if not user.is_active:
                return Response({"error": "This user is inactive."}, status=status.HTTP_400_BAD_REQUEST)
            
            token, created = Token.objects.get_or_create(user=user)
            user.login_count += 1
            user.current_login_at = timezone.now()
            user.current_login_ip = request.META.get('REMOTE_ADDR')
            user.save()
            
            return Response({
                "token": token.key,
                "user": CustomUserSerializer(user).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate a unique token
        reset_token = str(uuid.uuid4())
        user.reset_password_token = reset_token
        user.reset_password_sent_at = timezone.now()
        user.save()
        
        # Send email with the reset token
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
        send_mail(
            'Password Reset Request',
            f'Click the link below to reset your password:\n{reset_url}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        
        return Response({"message": "Password reset link has been sent to your email."}, status=status.HTTP_200_OK)
