from datetime import datetime, timedelta
from django.db import models


def cal_end_date():
    return datetime.now() + timedelta(days=6)


class Planet(models.Model):
    # user와 일대다관계
    # uidList = models.TextField()
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(default=cal_end_date)

    class Meta:
        ordering = ['id']
