from django.db import models
from testapp.models.custom_user import CustomUser


class UserActivity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    activity = models.CharField(max_length=100)
    time_stamp = models.DateTimeField(auto_now_add=True)
    role_name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(null=True, blank=True)