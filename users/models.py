from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django_resized import ResizedImageField
from planets.models import Planet
from quests.models import Quest
from django.db.models import CharField, Model
from django_mysql.models import ListCharField
from .managers import CustomUserManager
from django.db.models import Sum


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    registeredDate = models.DateTimeField(auto_now_add=True)
    lastlogined = models.DateTimeField(auto_now=True)
    nickname = models.CharField(max_length=12)


    level = models.IntegerField(default=1)
    rank = models.FloatField(default=0.0)

    report_user_cnt = models.IntegerField(default=0)     # 유저의 신고당한 횟수

    planet = models.ForeignKey(Planet, related_name='players', on_delete=models.SET_NULL, null=True)
    STATE = (
        ('N', 'Normal'),
        ('D', 'Dormant'),
        ('L', 'Leaved'),
    )
    state = models.CharField(max_length=10, choices=STATE, default='N')

    weekly_stats = models.CharField(max_length=10, default = '-')
    monthly_stats = models.FloatField(default=0.0)
    experience = models.FloatField(default = 0.0)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ('nickname',)
    
    def get_feed_cnt(self, planet=None):
        feeds = Feed.objects.filter(uid=self.id)
        if planet:
            feeds = feeds.filter(date__range=[planet.start_date, planet.end_date])
        return feeds.count()

    def get_distance(self, planet=None):
        feeds = Feed.objects.filter(uid=self.id)
        if planet:
            feeds = feeds.filter(date__range=[planet.start_date, planet.end_date])
        return feeds.aggregate(Sum('distance'))["distance__sum"] or 0

    def get_time(self, planet=None):
        feeds = Feed.objects.filter(uid=self.id)
        if planet:
            feeds = feeds.filter(date__range=[planet.start_date, planet.end_date])
        return feeds.aggregate(Sum('time'))["time__sum"] or 0

    def get_distance_for_level(self):
        feeds = Feed.objects.filter(uid=1)
        startday = datetime.datetime.now() - relativedelta(weekday=1)
        endday =  datetime.datetime.now()
        feeds = feeds.filter(date__range=[startday,endday])
        return feeds.aggregate(Sum('distance'))["distance__sum"] or 0

class Feed(Model):
    uid = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    title = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    distance = models.FloatField()  # "XX.XX"km단위
    time = models.IntegerField()    # "분"단위
    photo = ResizedImageField(size=[300,300],upload_to='',force_format='JPEG',quality=95)
    report_feed_cnt = models.IntegerField(default=0)     # 게시물의 신고당한 횟수
    report_uidList = ListCharField(
        base_field=CharField(max_length=10),
        size=6,
        max_length=(6 * 11),
        default = [] 
    )


class QuestList(models.Model):
    uid = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    qid = models.ForeignKey(Quest, on_delete = models.CASCADE)  # quest와 questlist는 1:N 관계
    STATE = (
        ('TODO', 'todo'),
        ('DOING', 'doing'),
        ('DONE', 'done'),
        ('ABANDON', 'abandon')  # 포기 Or 스킵 상태
    )
    state = models.CharField(max_length=10, choices=STATE, default='TODO')
    