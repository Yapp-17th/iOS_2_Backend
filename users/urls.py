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
    path('users/', include(User_router.urls)),
    path('feed/', include(Feed_router.urls)),
    path('questlist/', include(Questlist_router.urls)),
    path('rank_update/',views.rank_update),
    path('level_update/',views.level_update)
] 
