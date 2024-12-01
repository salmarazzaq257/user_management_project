from testapp.models.custom_user import CustomUser
from testapp.models.role_management import RoleManagement
from testapp.models.user_activity import UserActivity
from django.shortcuts import render



def admin_panel(request):
    users = CustomUser.objects.all()
    roles = RoleManagement.objects.all()
    activity_logs = UserActivity.objects.all()
    print(users, roles, activity_logs)  # Debugging print
    return render(request, 'index.html', {
        'users': users,
        'roles': roles,
        'activity_logs': activity_logs,
    })


