from django.db import models

class Quest(models.Model):
    title = models.CharField(max_length=800)
    content = models.TextField(max_length=1000)
    CATEGORY = (
        ('T' , 'training'),
        ('R' , 'routine'),
    )
    category = models.CharField(max_length=10, choices=CATEGORY, default='training')

    def __str__(self):
        return self.title
