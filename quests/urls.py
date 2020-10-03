from django.urls import path, include
from quests import views
from rest_framework import routers

quest_router = routers.DefaultRouter()
quest_router.register('',views.QuestViewSet)

urlpatterns = [
    path('quest/',include(quest_router.urls))
]
