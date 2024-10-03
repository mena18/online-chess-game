from __future__ import annotations
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, password2=None):
        if username is None:
            raise TypeError("Users should have a username")

        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None):
        if password is None:
            raise TypeError("Password should not be none")

        user = self.create_user(username=username, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    class Meta:
        # Define the table name using the db_table option
        db_table = "User"

    username = models.CharField(
        max_length=255, unique=True, db_index=True, null=True, blank=True
    )

    password = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def admin(self):
        return self.is_superuser

    @property
    def full_name(self):
        return self.client.full_name
