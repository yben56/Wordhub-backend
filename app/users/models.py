from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, null=True)
    birthday = models.DateField(blank=False, null=False)
    gender = models.BooleanField(blank=False, null=False)
    profile_picture = models.URLField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password', 'birthday', 'gender']

class UserResetPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
    used = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users_user_reset_password'