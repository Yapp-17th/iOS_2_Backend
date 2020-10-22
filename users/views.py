from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view, action
from .serializers import UserSerializer,FeedSerializer,QuestListSerializer
from .models import CustomUser,Feed,QuestList
from rest_framework.response import Response
import datetime



class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
    #닉네임 받기
    def update(self, request, *args, **kwargs): 
        nickname = request.data.get('nickname') 
        user_info  = self.get_object() 
        user_info.nickname = nickname 
        self.perform_update(user_info) 
        return Response(status=status.HTTP_201_CREATED)

    #lastlogined 갱신(앱실행시 호출)
    @action(detail=True, methods=['get'])
    def update_lastlogined(self, request, pk, *args, **kwargs):
        user_info = self.get_object()
        user_info.lastlogined = datetime.datetime.now()
        self.perform_update(user_info)
        return Response(status=status.HTTP_201_CREATED)
    
    #3일 미접속 유저 user state 변경, 신고유저 state 변경
    @action(detail=True, methods=['get'])
    def change_userstate(self,request, pk, *args, **kwargs):
        user_info = self.get_object()
        if datetime.datetime.now() == user_info.lastlogined + datetime.timedelta(days=3):
            user_info.state = "D"
            serializer = self.get_serializer(user_info)
            return Response(serializer.data)

    #신고기능
    @action(detail=True, methods=['get'])
    def report_user(self,request, pk, *args, **kwargs):
        user_info = self.get_object()
        user_info.report_user_cnt += 1
        self.perform_update(user_info)

        if user_info.report_user_cnt >= 3: 
            user_info.state = "L"
            serializer = self.get_serializer(user_info)
            return Response(serializer.data)


class FeedViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer

    #def perform_create(self,serializer):
    #    serializer.save(uid = self.request.user)

class QuestListViewSet(viewsets.ModelViewSet):
    queryset = QuestList.objects.all()
    serializer_class = QuestListSerializer

#랭크 업데이트
@api_view(['GET'])
def rank_update(request):
    user_info = CustomUser.objects.all()
    serializer = UserSerializer(user_info)
    serializer.rank_save(user_info)
    return Response(serializer.data)