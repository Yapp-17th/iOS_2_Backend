from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('users/', include('users.urls')),
    path('quests/', include('quests.urls')),
    path('planets/', include('planets.urls')),
]
