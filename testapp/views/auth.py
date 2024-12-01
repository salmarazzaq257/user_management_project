# from rest_framework.authtoken.models import Token
# from testapp.models import CustomUser
# from datetime import timedelta
# from django.utils import timezone
# import logging
# from django.contrib.auth import authenticate
# from django.shortcuts import render
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.response import Response
# from rest_framework import status
# from testapp.serializers.user_serializers import CustomUserSerializer
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from testapp.serializers.auth import AuthSerializer
# from django.core.mail import send_mail
# from django.conf import settings
# import uuid
# from rest_framework.authtoken.models import Token
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from testapp.models import CustomUser




# logger = logging.getLogger(__name__)

# def index(request):
#     return render(request, 'index.html')


# class UserLoginView(APIView):
#     @swagger_auto_schema(request_body=AuthSerializer)
#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         password = request.data.get('password')
        
#         user = authenticate(email=email, password=password)
        
#         if user is not None:
#             if user.deleted_at is not None:
#                 return Response({"error": "This user has been deleted."}, status=status.HTTP_400_BAD_REQUEST)
            
#             if not user.is_active:
#                 return Response({"error": "This user is inactive."}, status=status.HTTP_400_BAD_REQUEST)
            
#             token, created = Token.objects.get_or_create(user=user)
#             user.login_count += 1
#             user.current_login_at = timezone.now()
#             user.current_login_ip = request.META.get('REMOTE_ADDR')
#             user.save()
            
#             return Response({
#                 "token": token.key,
#                 "user": CustomUserSerializer(user).data
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)


# class ResetPasswordView(APIView):
#     @swagger_auto_schema(request_body=AuthSerializer)
#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
        
#         try:
#             user = CustomUser.objects.get(email=email)
#         except CustomUser.DoesNotExist:
#             return Response({"error": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Generate a unique token
#         reset_token = str(uuid.uuid4())
#         user.reset_password_token = reset_token
#         user.reset_password_sent_at = timezone.now()
#         user.save()
        
#         # Send email with the reset token
#         reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
#         send_mail(
#             'Password Reset Request',
#             f'Click the link below to reset your password:\n{reset_url}',
#             settings.DEFAULT_FROM_EMAIL,
#             [email],
#             fail_silently=False,
#         )
        
#         return Response({"message": "Password reset link has been sent to your email."}, status=status.HTTP_200_OK)


# class GetToken(ObtainAuthToken):
#     @method_decorator(csrf_exempt)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)
    
#     def post(self, request):
#         """
#         Handle POST request to generate or retrieve a token for a user.
#         """
#         identifier = request.data.get("identifier")
#         field = request.data.get("field", "email")  # Default to email if not provided

#         if not identifier:
#             logger.error("Identifier not provided in the request.")
#             return Response({"error": "Identifier not provided."}, status=status.HTTP_400_BAD_REQUEST)

#         # Validate the field parameter
#         valid_fields = ["email", "username"]
#         if field not in valid_fields:
#             logger.error(f"Invalid field '{field}' provided.")
#             return Response(
#                 {"error": f"Invalid field '{field}'. Valid fields are {valid_fields}."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         try:
#             # Ensure the query is correctly constructed
#             user = CustomUser.objects.get(**{field: identifier})  # Use field as the key and identifier as the value
#         except CustomUser.DoesNotExist:
#             logger.error(f"User with {field}='{identifier}' does not exist.")
#             return Response(
#                 {"error": f"User with {field}='{identifier}' does not exist."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         # Retrieve or regenerate token
#         token = self._get_or_regenerate_token(user, identifier)

#         return Response({"token": token.key}, status=status.HTTP_200_OK)

#     @staticmethod
#     def _get_or_regenerate_token(user, identifier):
#         """
#         Retrieve an existing token or regenerate it if it is older than 6 hours.
#         """
#         token, created = Token.objects.get_or_create(user=user)
    
#         if not created:
#             utc_now = timezone.now()  # Use timezone-aware datetime
#             # Check if the token is older than 6 hours and regenerate if necessary
#             if token.created < utc_now - timedelta(hours=6):
#                 logger.info(f"Regenerating token for user: {identifier}")
#                 token.delete()
#                 token, created = Token.objects.get_or_create(user=user)
    
#         return token

#     @classmethod
#     def get_token(cls, identifier, field="email"):
#         """
#         Generate or retrieve a token for a user programmatically.
#         """
#         try:
#             user = CustomUser.objects.get(**{field: identifier})
#         except CustomUser.DoesNotExist:
#             logger.error(f"User with {field}='{identifier}' does not exist.")
#             raise ValueError(f"User with {field}='{identifier}' does not exist.")

#         return cls._get_or_regenerate_token(user, identifier)


from django.contrib.auth.backends import BaseBackend, ModelBackend
from testapp.models import CustomUser

from datetime import timedelta
import logging
import uuid
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from testapp.models import CustomUser
from testapp.serializers.auth import AuthSerializer
from testapp.serializers.user_serializers import CustomUserSerializer
import logging
logger = logging.getLogger(__name__)

# Home page
def index(request):
    return render(request, 'index.html')


class UserLoginView(APIView):
    """
    Handles user login by validating credentials and generating an authentication token.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=AuthSerializer)
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


class ResetPasswordView(APIView):
    """
    Handles password reset by generating a unique token and sending an email.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=AuthSerializer)
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Generate a unique token
        reset_token = str(uuid.uuid4())
        user.reset_password_token = reset_token
        user.reset_password_sent_at = timezone.now()
        user.save()

        # Send email with the reset token
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
        try:
            send_mail(
                'Password Reset Request',
                f'Click the link below to reset your password:\n{reset_url}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Failed to send reset email: {str(e)}")
            return Response({"error": "Failed to send reset email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Password reset link has been sent to your email."}, status=status.HTTP_200_OK)


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











# Update the backend to use email instead of username for authentication

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = get_user_model().objects.get(email=username)
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            return None
        return None

