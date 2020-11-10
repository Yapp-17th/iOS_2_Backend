from django.urls import path, include
from users import views
from rest_framework import routers
from push_notifications.api.rest_framework import APNSDeviceAuthorizedViewSet

User_router = routers.DefaultRouter()
User_router.register('', views.UserViewSet)
Feed_router = routers.DefaultRouter()
Feed_router.register('', views.FeedViewSet)
Questlist_router = routers.DefaultRouter()
Questlist_router.register('', views.QuestListViewSet) 
push_router = routers.DefaultRouter()
push_router.register(r'device/apns', APNSDeviceAuthorizedViewSet)

urlpatterns = [
    path('', include('rest_auth.urls')),    # login/, logout/, ...
    path('registration/', include('rest_auth.registration.urls')),

    path('quest_to_user/', views.quest_to_user),

    path('feed/', include(Feed_router.urls)),
    path('questlist/', include(Questlist_router.urls)),
    path('rank_update/',views.rank_update),
    path('level_update/',views.level_update),
    path('', include(User_router.urls)),
    #path('device/apns/', include(push_router.urls)),
]

