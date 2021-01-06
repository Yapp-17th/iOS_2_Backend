from django.contrib import admin
from .models import CustomUser,Feed, QuestList

admin.site.register(CustomUser)

admin.site.register(Feed)
admin.site.register(QuestList)