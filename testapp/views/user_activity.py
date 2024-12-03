import csv
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status, permissions
from testapp.models.user_activity import UserActivity
from testapp.serializers.user_activity_serilaizers import UserActivitySerializer

from datetime import datetime

class LogActivityView(APIView):
   
    permission_classes = [permissions.IsAdminUser]

    
    def post(self, request, *args, **kwargs):
        """
        Log a user activity.
        """
        serializer = UserActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

    
    def get(self, request, *args, **kwargs):
        """
        Retrieve user activity logs with optional filters for date range, user, role, and action type.
        """
        # Apply filters based on query parameters
        filters = {}

        # Filter by user if specified
        user_id = request.query_params.get('user_id', None)
        if user_id:
            filters['user_id'] = user_id

        # Filter by role if specified
        role_name = request.query_params.get('role_name', None)
        if role_name:
            filters['role_name'] = role_name

        # Filter by action type if specified
        action_type = request.query_params.get('action_type', None)
        if action_type:
            filters['action_type'] = action_type

        # Filter by date range if specified
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        if start_date:
            filters['timestamp__gte'] = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            filters['timestamp__lte'] = datetime.strptime(end_date, '%Y-%m-%d')

        # Get filtered user activity logs
        user_activity = UserActivity.objects.filter(**filters)
        serializer = UserActivitySerializer(user_activity, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def export_csv(self, request, *args, **kwargs):
        """
        Export user activity logs as a CSV file with optional filters.
        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user_activity_logs.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Full Name', 'Email', 'Activity', 'Action Type', 'Timestamp', 'Role Name', 'IP Address', 'User ID'])

        # Apply filters as before
        filters = {}

        user_id = request.query_params.get('user_id', None)
        if user_id:
            filters['user_id'] = user_id

        role_name = request.query_params.get('role_name', None)
        if role_name:
            filters['role_name'] = role_name

        action_type = request.query_params.get('action_type', None)
        if action_type:
            filters['action_type'] = action_type

        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        if start_date:
            filters['timestamp__gte'] = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            filters['timestamp__lte'] = datetime.strptime(end_date, '%Y-%m-%d')

        # Stream user activities to avoid memory issues for large datasets
        queryset = UserActivity.objects.filter(**filters).iterator()

        for activity in queryset:
            writer.writerow([
                activity.id,
                activity.full_name,
                activity.email,
                activity.action_type,
                activity.timestamp,
                activity.role_name,
                activity.ip_address,
                activity.user
            ])

        return response
