from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    registeredDate = models.DateTimeField(auto_now_add=True)
    nickname = models.CharField(max_length=10)

    level = models.IntegerField(default=1)
    rank = models.FloatField(default=0.0)

    # planet 아직
    STATE = (
        ('N', 'Normal'),
        ('D', 'Dormant'),
        ('L', 'Leaved'),
    )
    state = models.CharField(max_length=10, choices=STATE, default='N')

    def __str__(self):
        return self.email
