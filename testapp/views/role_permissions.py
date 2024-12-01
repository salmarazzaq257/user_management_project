from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdmi
from rest_framework import status
from testapp.models.role_permission import RolePermission
from testapp.serializers.role_permission_serializers import RolePermissionSerializer
from drf_yasg.utils import swagger_auto_schema

class RolePermissionsView(APIView):
    permission_classes = [IsAdminUser]


    @swagger_auto_schema(request_body=RolePermissionSerializer)
    def post(self, request, *args, **kwargs):
        serializer = RolePermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
