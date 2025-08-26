from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
class CustomUserManager(BaseUserManager):
    """Manager where email is the unique identifier for authentication."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with given email & password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Custom user model that uses email as username field."""

    username = models.CharField(max_length=150, blank=True)  # optional display name
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"   # login with email
    REQUIRED_FIELDS = []       # no extra fields required on createsuperuser

    objects = CustomUserManager()

    def __str__(self):
        return self.email

