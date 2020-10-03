from django.db import models

class Planet(models.Model):
    uidList = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
