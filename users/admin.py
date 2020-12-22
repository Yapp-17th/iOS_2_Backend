from django.contrib import admin
from .models import CustomUser,Feed

admin.site.register(CustomUser)

admin.site.register(Feed)