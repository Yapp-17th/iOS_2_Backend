from django.urls import path, include
from trashcans import views
from rest_framework import routers

trashcan_router = routers.DefaultRouter()
trashcan_router.register('', views.TrashcanViewSet)

urlpatterns = [
    # path('get_trashcan/', views.get_trashcan_csv),
    path('', include(trashcan_router.urls)),
]
