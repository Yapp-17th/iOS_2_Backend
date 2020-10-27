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

class FeedViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    
    #신고기능_피드
    @action(detail=True, methods=['get'])
    def report_feed(self,request, pk, *args, **kwargs):
        feed_info = self.get_object()
        report_user = CustomUser.objects.get(id=1)

        #중복방지
        if str(report_user.id) not in feed_info.report_uidList: 
            feed_info.report_uidList.append(report_user.id)
            self.perform_update(feed_info)
            #3번째 신고면 삭제
            if len(feed_info.report_uidList) >= 3: 
                self.perform_destroy(feed_info)
                return Response(status = status.HTTP_202_ACCEPTED)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)

        

class QuestListViewSet(viewsets.ModelViewSet):
    queryset = QuestList.objects.all()
    serializer_class = QuestListSerializer

#랭크 업데이트 (report_feed 실행후, 새로고침 실행후 호출)
@api_view(['GET'])
def rank_update(request):
    user_info = CustomUser.objects.all()
    serializer = UserSerializer(user_info)
    serializer.rank_save(user_info)
    return Response(status = status.HTTP_202_ACCEPTED)

#레벨 업데이트(새로고침 실행후 호출)
@api_view(['GET'])
def level_update(request,self, *args, **kwargs):
    user_info = CustomUser.objects.get(id = self.request.user.id)
    serializer = UserSerializer(user_info)
    serializer.level_save(user_info)
    return Response(serializer.data,status = status.HTTP_202_ACCEPTED)