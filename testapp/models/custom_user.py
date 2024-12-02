from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.models import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from testapp.models.role_management import RoleManagement

# Create your models here.

class CustomUser(AbstractUser):
    role = models.ForeignKey(RoleManagement, related_name="management_user", on_delete=models.CASCADE)

    def has_permission(self, perm_code):
        return self.role and self.role.permissions.filter(code=perm_code).exists()
    
    email = models.EmailField(unique=True)
    is_confirmed = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    current_login_in = models.DateTimeField(null=True, blank=True)
    current_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_login_in = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    reset_password_token = models.CharField(max_length=100, null=True, blank=True)
    reset_password_sent_at = models.DateTimeField(null=True, blank=True)
    remember_created_at = models.DateTimeField(null=True, blank=True)
    login_count = models.IntegerField(default=0)


    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def soft_delete(self):
        self.deleted_at = now()  # Set the current timestamp
        self.is_deleted = True   # Mark as deleted
        self.save()
    def __str__(self):
        return self.email
    
    def is_token_expired(self):
        if not self.reset_password_sent_at:
            return True  # Treat as expired if the timestamp is missing
        return now() - self.reset_password_sent_at > timedelta(hours=1)
    
    
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


