from django.db import models
from testapp.models.role_management import RoleManagement


class RolePermission(models.Model):
    role = models.ForeignKey(RoleManagement, on_delete=models.CASCADE)
    main_module = models.CharField(max_length=100)
    module_name = models.CharField(max_length=100)
    view_access= models.BooleanField(default=False)
    create_access = models.BooleanField(default=False)
    update_access = models.BooleanField(default=False)
    delete_access = models.BooleanField(default=False)