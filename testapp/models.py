# from django.db import models
# from django.contrib.auth.models import AbstractUser, Group, Permission
# from datetime import datetime
# from django.contrib.auth.models import UserManager
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token
# from django.conf import settings
# from testapp.models.role_management import RoleManagement

# # Create your models here.

    

# class CustomUser(AbstractUser):
#     role = models.ForeignKey(RoleManagement, related_name="management_user", on_delete=models.CASCADE)
       
#     email = models.EmailField(unique=True)
#     is_confirmed = models.BooleanField(default=False)
#     deleted_at = models.DateTimeField(null=True, blank=True)
#     is_deleted = models.BooleanField(default=False)
#     current_login_in = models.DateTimeField(null=True, blank=True)
#     current_login_ip = models.GenericIPAddressField(null=True, blank=True)
#     last_login_in = models.DateTimeField(null=True, blank=True)
#     last_login_ip = models.GenericIPAddressField(null=True, blank=True)
#     reset_password_token = models.CharField(max_length=100, null=True, blank=True)
#     reset_password_sent_at = models.DateTimeField(null=True, blank=True)
#     remember_created_at = models.DateTimeField(null=True, blank=True)
#     login_count = models.IntegerField(default=0)


#     objects = UserManager()
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []


#     def soft_delete(self):
#         self.deleted_at = True
#         self.save()
    
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)




    
# # raising conflict:SystemCheckError: System check identified some issues:due to the custome user and auth.user so need to add group and permission



