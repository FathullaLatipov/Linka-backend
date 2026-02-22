from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Phone number required")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone,password,**extra_fields)

class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = None
    # E.164 format (+998901234567) для OTP-flow; legacy: 9 цифр
    phone = models.CharField(max_length=20, null=False, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone


# Хранение OTP для верификации.
# В production: использовать Redis/cache (ключ verify_id -> {phone, otp, expires_at})
# Rate limiting: добавить throttle (например ThrottleAnonRate) на SendOTPView и VerifyOTPView
class OTPCode(models.Model):
    verify_id = models.CharField(max_length=36, unique=True, db_index=True)
    phone = models.CharField(max_length=20)
    otp_code = models.CharField(max_length=10)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "otp_codes"
        ordering = ["-created_at"]

    def is_expired(self):
        return timezone.now() >= self.expires_at


