from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager


class TemporalOwnerManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self,  password, **extra_fields):
        """Creates custom is_admin=True user. Password is required"""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_admin", True)
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, password=None, **extra_fields):
        """Creates regular user"""
        extra_fields.setdefault("is_admin", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(password, **extra_fields)

    def create_superuser(self, password, **extra_fields):
        """Creates django SuperUser. Password is required"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(password, **extra_fields)


class TemporalOwner(AbstractBaseUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} - {self.last_name} , {self.city}"

    def save(self, *args, **kwargs):
        if self.is_superuser and not self.is_admin:
            self.is_admin = True
        if self.is_admin and not self.password:
            raise ValueError("Admin must have a password.")

        super().save(*args, **kwargs)

    def check_owner_password(self, password):
        return self.password == password

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    objects = TemporalOwnerManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []




