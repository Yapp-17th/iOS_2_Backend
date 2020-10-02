from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('users/', include('users.urls')),
    path('accounts/', include('accounts.urls')),
    path('quests/', include('quests.urls')),
    path('planets/', include('planets.urls')),
    path('trashcans/', include('trashcans.urls')),

    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]
