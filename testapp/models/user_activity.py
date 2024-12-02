from django.db import models
from testapp.models.custom_user import CustomUser


class UserActivity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    action_type = models.CharField(max_length=100)  # E.g., Create, Update, Delete
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    role_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Activity by {self.full_name} ({self.email}) on {self.timestamp}"