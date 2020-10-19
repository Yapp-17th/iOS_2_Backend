from django.urls import path, include
from users import views
from rest_framework import routers

User_router = routers.DefaultRouter()
User_router.register('', views.UserViewSet)
Feed_router = routers.DefaultRouter()
Feed_router.register('', views.FeedViewSet)
Questlist_router = routers.DefaultRouter()
Questlist_router.register('', views.QuestListViewSet)

urlpatterns = [
    path('feed/', include(Feed_router.urls)),
    path('questlist/', include(Questlist_router.urls)),
    path('', include(User_router.urls)),
] 
