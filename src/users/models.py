from django.utils import timezone
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator

from src.choices.common import Position


class User(AbstractBaseUser, PermissionsMixin):
    username: str = models.CharField(
        _('username'),
        max_length=50,
        unique=True)
    first_name: str = models.CharField(
        _('first_name'),
        max_length=50,
        validators=[MinLengthValidator(2)])
    last_name: str = models.CharField(
        _('last_name'),
        max_length=50,
        validators=[MinLengthValidator(2)])
    email: str = models.EmailField(
        _('email'),
        unique=True
    )
    phone_number: str = models.CharField(
        max_length=20,
        validators=[MinLengthValidator(8)])
    position: str = models.CharField(
        _('position'),
        max_length=50,
        choices=Position.choices())
    is_staff: bool = models.BooleanField(
        default=False
    )
    is_active: bool = models.BooleanField(
        default=True
    )
    date_joined: timezone = models.DateTimeField(
        auto_now_add=True)
    updated_at: timezone = models.DateTimeField(
        auto_now=True
    )
    deleted: bool = models.BooleanField(
        default=False
    )
    deleted_at: timezone = models.DateTimeField(
        blank=True,
        null=True
    )
    main_project = models.ForeignKey(
        'projects.Project',
        on_delete=models.SET_NULL,
        null=True,
        related_name="main_staff"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username",
                       "first_name",
                       "last_name",
                       "position"]

    objects = UserManager()

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

