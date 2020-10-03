from django.urls import path, include
from planets import views
from rest_framework import routers

planet_router = routers.DefaultRouter()
planet_router.register('',views.PlanetViewSet)

urlpatterns = [
    path('planet/',include(planet_router.urls))
]
