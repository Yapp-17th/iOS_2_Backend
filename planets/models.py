from datetime import datetime, timedelta
from django.db import models


def cal_end_date():
    return datetime.now() + timedelta(days=6)


class Planet(models.Model):
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(default=cal_end_date)
    user_cnt = models.IntegerField(default=0)

    class Meta:
        ordering = ['id']
