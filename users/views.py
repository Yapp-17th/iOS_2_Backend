from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view
from .serializers import UserSerializer,FeedSerializer,QuestListSerializer
from .models import CustomUser,Feed,QuestList
from rest_framework.response import Response

from rest_framework.authentication import BasicAuthentication 

class UserViewSet(viewsets.ModelViewSet, mixins.UpdateModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    

class FeedViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer

    #def perform_create(self,serializer):
    #    serializer.save(uid = self.request.user)

class QuestListViewSet(viewsets.ModelViewSet):
    queryset = QuestList.objects.all()
    serializer_class = QuestListSerializer

@api_view(['GET'])
def rank_update(request):
    user_info = CustomUser.objects.all()
    serializer = UserSerializer(user_info)
    serializer.rank_save(user_info)
    return Response(serializer.data)