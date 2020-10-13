from django.db import models

class Planet(models.Model):
    # user와 일대다관계
    # uidList = models.TextField()
    user_cnt = models.IntegerField(default=1)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
