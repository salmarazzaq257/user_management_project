
from testapp.models import CustomUser
from datetime import timedelta
import logging
import secrets
from django.conf import settings
from django.contrib.auth import authenticate,  hashers
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from testapp.models import CustomUser
from testapp.serializers.auth import AuthSerializer
from testapp.serializers.user_serializers import CustomUserSerializer
import logging
logger = logging.getLogger(__name__)




class UserLoginView(APIView):
    """
    Handles user login by validating credentials and generating an authentication token.
    """
    permission_classes = [AllowAny]

   
    def post(self, request, *args, **kwargs):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        remember_me = serializer.validated_data.get('remember_me', False)  # Optionally handle remember me

        user = authenticate(email=email, password=password)

        if user:
            # Check if the user is confirmed
            if not user.is_confirmed:
                return Response({"error": "Email is not confirmed."}, status=status.HTTP_400_BAD_REQUEST)

            if user.deleted_at:
                return Response({"error": "This user has been deleted."}, status=status.HTTP_400_BAD_REQUEST)

            if not user.is_active:
                return Response({"error": "This user is inactive."}, status=status.HTTP_400_BAD_REQUEST)

            # Handle "Remember Me" functionality
            if remember_me:
                # Set the session to last for a longer period (e.g., 2 weeks)
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                # Default session expiry (browser session)
                request.session.set_expiry(0)

            token, created = Token.objects.get_or_create(user=user)
            user.login_count += 1
            user.current_login_at = timezone.now()
            user.current_login_ip = request.META.get('REMOTE_ADDR')
            user.save()

            return Response({
                "token": token.key,
                "user": CustomUserSerializer(user).data
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)
    

class GenerateResetTokenView(APIView):
    permission_classes = [IsAuthenticated]

   

  
    def post(self, request, *args, **kwargs):
        user = request.user  # Get the currently authenticated user
        token = secrets.token_hex(32)  # Generate a secure random token
        user.reset_password_token = token  # Set the token on the user instance
        user.reset_password_sent_at = timezone.now()  # Set the token generation timestamp
        user.save()  # Save the changes to the database

        return Response({"detail": "Password reset token generated", "token": token}, status=status.HTTP_200_OK)


class ResetPasswordWithTokenView(APIView):

    def post(self, request, *args, **kwargs):
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        # Check if the token exists in the database
        try:
            user = CustomUser.objects.get(reset_password_token=token)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the token has expired
        if user.is_token_expired():
            return Response({"detail": "Token has expired"}, status=status.HTTP_400_BAD_REQUEST)

        # Reset the user's password
        user.set_password(new_password)  # Automatically hashes the password
        user.reset_password_token = None  # Invalidate the token
        user.reset_password_sent_at = None  # Clear the token timestamp
        user.save()

        return Response({"detail": "Password reset successfully"}, status=status.HTTP_200_OK)

class GetToken(ObtainAuthToken):
    """
    Handles token generation and regeneration for users.
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        identifier = request.data.get("identifier")
        field = request.data.get("field", "email")

        if not identifier:
            logger.error("Identifier not provided in the request.")
            return Response({"error": "Identifier not provided."}, status=status.HTTP_400_BAD_REQUEST)

        valid_fields = ["email", "username"]
        if field not in valid_fields:
            logger.error(f"Invalid field '{field}' provided.")
            return Response(
                {"error": f"Invalid field '{field}'. Valid fields are {valid_fields}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = CustomUser.objects.get(**{field: identifier})
        except CustomUser.DoesNotExist:
            logger.error(f"User with {field}='{identifier}' does not exist.")
            return Response({"error": f"User with {field}='{identifier}' does not exist."}, status=status.HTTP_404_NOT_FOUND)

        token = self._get_or_regenerate_token(user)

        return Response({"token": token.key}, status=status.HTTP_200_OK)

    @staticmethod
    def _get_or_regenerate_token(user):
        token, created = Token.objects.get_or_create(user=user)

        if not created:
            utc_now = timezone.now()
            token_expiry_hours = getattr(settings, 'TOKEN_EXPIRY_HOURS', 6)
            if token.created < utc_now - timedelta(hours=token_expiry_hours):
                logger.info(f"Regenerating token for user: {user}")
                token.delete()
                token, created = Token.objects.get_or_create(user=user)

        return token

    @classmethod
    def get_token(cls, identifier, field="email"):
        try:
            user = CustomUser.objects.get(**{field: identifier})
        except CustomUser.DoesNotExist:
            logger.error(f"User with {field}='{identifier}' does not exist.")
            raise ValueError(f"User with {field}='{identifier}' does not exist.")

        return cls._get_or_regenerate_token(user)










