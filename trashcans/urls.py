from django.urls import path, include
from trashcans import views
from rest_framework import routers

trashcan_router = routers.DefaultRouter()
trashcan_router.register('', views.TrashcanViewSet)

urlpatterns = [
    path('', include(trashcan_router.urls)),
]
