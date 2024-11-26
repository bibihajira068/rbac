from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models

class MyManager(BaseUserManager):
    
    def create_user(self, email, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password=password, **extra_fields)

class User(AbstractUser, PermissionsMixin):
    
    email = models.EmailField(unique=True) 
    profile_picture = models.URLField(blank=True, null=True, help_text="URL to the user's Google profile picture")
    bio = models.TextField(blank=True, null=True, help_text="Optional user bio")
    date_of_birth = models.DateField(blank=True, null=True, help_text="Optional DOB")
    google_id = models.CharField(max_length=100, blank=True, null=True, unique=True, help_text="Google OAuth ID")
    profile_picture = models.URLField(blank=True, null=True, help_text="URL to the user's Google profile picture")
    is_google_authenticated = models.BooleanField(default=False, help_text="Whether the user logged in via Google")
    
    objects = MyManager()

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['username'] 
    def _str_(self):
        return self.email