from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.contrib import auth
from django.conf import settings
from quests.models import Quest
from planets.models import Planet

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    registeredDate = models.DateTimeField(auto_now_add=True)
    lastlogined = models.DateTimeField(auto_now=True)
    nickname = models.CharField(max_length=10)

    level = models.IntegerField(default=1)
    rank = models.FloatField(default=0.0)

    report_user_cnt = models.IntegerField(default=0)     # 유저의 신고당한 횟수
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE, null=True)

    STATE = (
        ('N', 'Normal'),
        ('D', 'Dormant'),
        ('L', 'Leaved'),
    )
    state = models.CharField(max_length=10, choices=STATE, default='N')

    def __str__(self):
        return self.email


class Feed(models.Model):
    uid = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    title = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)  
    photo = models.ImageField()
    report_feed_cnt = models.IntegerField(default=0)     # 게시물의 신고당한 횟수


class QuestList(models.Model):
    uid = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    qid = models.ForeignKey(Quest, on_delete = models.CASCADE)
    STATE = (
        ('TODO', 'todo'),
        ('DOING', 'doing'),
        ('DONE', 'done'),
        ('ABANDON', 'abandon')  # 포기 Or 스킵 상태
    )
    state = models.CharField(max_length=10, choices=STATE, default='TODO')