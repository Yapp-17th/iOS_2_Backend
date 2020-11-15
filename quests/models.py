from django.db import models

class Quest(models.Model):
    title = models.CharField(max_length=800)
    content = models.TextField(max_length=1000)
    CATEGORY = (
        ('T' , 'training'),
        ('R' , 'routine'),
    )
    category = models.CharField(max_length=10, choices=CATEGORY, default='training')
    step = models.IntegerField(default=0)   # 트레이닝일때 필요, 목표달성은 다 0으로

    def __str__(self):
        return self.title
