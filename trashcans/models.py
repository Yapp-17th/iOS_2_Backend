from django.db import models
from users.models import CustomUser
from django.conf import settings

class Trashcan(models.Model):
    #MYSQL 에서는 Floatfield -> Double 데이터타입 생성
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    address = models.TextField()
    STATE = (
        ('C','confirmed'), 
        ('NC','notConfirmed')
    )
    state = models.CharField(max_length=15, choices=STATE, default='NC')
    delete_cnt = models.IntegerField(default=0)     # 삭제 요청 횟수
