from django.db import models



class RoleManagement(models.Model):
    role_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.role_name