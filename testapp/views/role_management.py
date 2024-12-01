from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from testapp.models.role_management import RoleManagement
from testapp.serializers.role_serializers import RoleManagementSerializer
from drf_yasg.utils import swagger_auto_schema 
from utils.custom_pagination import CustomPagination

class RolePagination(CustomPagination):
    pagination_class = CustomPagination
    


class RoleManagementiew(APIView):

    
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(request_body=RoleManagementSerializer)

    def post(self, request, *args, **kwargs):
        serializer = RoleManagementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateRoleView(APIView):
    permission_classes = [IsAdminUser]
    @swagger_auto_schema(request_body=RoleManagementSerializer)
    def put(self, request, id, *args, **kwargs):
        role = RoleManagement.objects.get(id=id)
        serializer = RoleManagementSerializer(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListRolesView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        roles = RoleManagement.objects.all()
        serializer = RoleManagementSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
