import rest_framework.authtoken.apps
from hashid_field import HashidField

from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin, AnonymousUser,
)
from django.db import models
from django.utils import timezone

UNINITIALIZED_POSITION = -1



class UserManager(BaseUserManager):
    def _create_user(self, email, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        user = self.model(
            email=self.normalize_email(email),
            is_active=True,
            is_staff=is_staff,
            is_superuser=is_superuser,
            last_login=timezone.now(),
            registered_at=timezone.now(),
            **extra_fields,
        )
        user.set_unusable_password() # password is managed by firebase so we don't store a password
        user.save(using=self._db)
        return user

    def create_user(self, email=None, **extra_fields):
        is_staff = extra_fields.pop("is_staff", False)
        is_superuser = extra_fields.pop("is_superuser", False)
        return self._create_user(
            email, is_staff, is_superuser, **extra_fields
        )

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(
            email, password, is_staff=True, is_superuser=True, **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="Email", unique=True, max_length=255)
    first_name = models.CharField(
        verbose_name="First name", max_length=30, default="first"
    )
    last_name = models.CharField(
        verbose_name="Last name", max_length=30, default="last"
    )
    avatar = models.ImageField(verbose_name="Avatar", blank=True)

    is_admin = models.BooleanField(verbose_name="Admin", default=False)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    is_staff = models.BooleanField(verbose_name="Staff", default=False)
    registered_at = models.DateTimeField(
        verbose_name="Registered at", auto_now_add=timezone.now
    )

    # Fields settings
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    full_name.fget.short_description = "Full name"

    @property
    def short_name(self):
        return f"{self.last_name} {self.first_name[0]}."

    short_name.fget.short_description = "Short name"

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.short_name

    def __str__(self):
        return self.full_name


class WaitlistUser(models.Model):
    first_name = models.CharField(
        verbose_name="First name", max_length=30, default=None, null=True, blank=True
    )
    email = models.EmailField(verbose_name="Email", unique=True, max_length=255)
    can_register = models.BooleanField(default=False, verbose_name="Can Register")
    waitlist_join_dt = models.DateTimeField(
        verbose_name="Waitlist Joined Datetime", auto_now_add=timezone.now,
    )
    current_position = models.IntegerField(verbose_name="Current Position on Waitlist", default=UNINITIALIZED_POSITION)
    referral_id = HashidField(null=True, blank=True)
    referrer_id = models.IntegerField(verbose_name="Primary Key of Referrer", default=None, blank=True, null=True)

def create_waitlist_user(email: str, referree_id: str, first_name: str):
    waitlist_user = WaitlistUser.objects.create(
        email=BaseUserManager.normalize_email(email),
        first_name=first_name
    )
    waitlist_user.referral_id = waitlist_user.id
    if referree_id:
        try:
            referral_user = WaitlistUser.objects.get(referral_id=referree_id)
            waitlist_user.referree_id = referral_user.id
            print(f"referree_id {referree_id} was found; referree was {referral_user.email}")
        except WaitlistUser.DoesNotExist:
            print(f"Given referree_id {referree_id} can not be found")
            pass
    waitlist_user.save()
    return waitlist_user
