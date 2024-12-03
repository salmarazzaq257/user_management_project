from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from testapp.models.custom_user import CustomUser
from testapp.models.role_management import RoleManagement
from testapp.serializers.user_serializers import CustomUserSerializer
from django.contrib.auth.hashers import make_password
import logging
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)

# Helper method to fetch user or return not found response
def get_user_or_404(user_id):
    return get_object_or_404(CustomUser, id=user_id)

class CreateUserView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request, *args, **kwargs):
        # Pass the data to the serializer
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            # Ensure role exists if provided
            role = request.data.get("role")
            if role:
                role_instance = RoleManagement.objects.filter(id=role).first()
                if not role_instance:
                    return Response({"detail": "Role not found."}, status=status.HTTP_400_BAD_REQUEST)
                serializer.validated_data["role"] = role_instance

            # Hash password before saving
            password = request.data.get("password")
            if password:
                serializer.validated_data["password"] = make_password(password)

            # Save the user
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Return error if serializer is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListUsersView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, *args, **kwargs):
        search_query = request.query_params.get("search", None)
        is_active = request.query_params.get("is_active", None)
        role = request.query_params.get("role", None)

        # Base queryset
        queryset = CustomUser.objects.all()

        # Apply filters
        if search_query:
            queryset = queryset.filter(email__icontains=search_query) | queryset.filter(username__icontains=search_query)
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
        if role:
            queryset = queryset.filter(role_id=role)

        # Serialize data
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateUserView(APIView):
    permission_classes = [IsAdminUser]

  
    
    def put(self, request, id, *args, **kwargs):
        user = get_user_or_404(id)  # This function should fetch the user or return 404
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id, *args, **kwargs):
        user = get_user_or_404(id)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)  # Use `partial=True` for partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ActivationView(APIView):

    permission_classes = [IsAdminUser]

    def patch(self, request, id, *args, **kwargs):
        """
        Toggle the activation status of the user identified by the ID.
        """
        try:
            # Retrieve the user
            user = CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Toggle the `is_active` status
        user.is_active = not user.is_active
        user.save()

        status_message = "activated" if user.is_active else "deactivated"
        logger.info(f"User {user.email} has been {status_message} by admin.")
        return Response({"detail": f"User successfully {status_message}."}, status=status.HTTP_200_OK)
class DeleteUserView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, id, *args, **kwargs):
        user = CustomUser.objects.get(id=id)
        user.soft_delete()  # Using the soft delete method
        return Response({"detail": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

       