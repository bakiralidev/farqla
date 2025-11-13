# apps/userapp/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator

uz_phone_validator = RegexValidator(
    regex=r"^\+998\d{9}$",
    message="Telefon +998XXXXXXXXX formatida bo‘lishi kerak."
)

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Phone majburiy")
        phone = self.normalize_email(phone) if phone.startswith("@") else phone  # no-op, faqat safety
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True or extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser uchun is_staff=True va is_superuser=True kerak")
        return self.create_user(phone, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    name  = models.CharField(max_length=120, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=13, unique=True, validators=[uz_phone_validator])

    # standart django flaglari
    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD  = "phone"     # login shu bilan
    REQUIRED_FIELDS = []          # createsuperuser paytida faqat phone + password

    def __str__(self):
        return self.phone
