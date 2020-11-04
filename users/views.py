from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view, action

from quests.models import Quest
from .serializers import UserSerializer, FeedSerializer, QuestListSerializer, QuestListDetailSerializer
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
        report_user = CustomUser.objects.get(id=self.request.user.id)

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
    http_method_names = ['get', 'head']

    # 퀘스트 상세 설명 화면, 학습퀘스트일 경우 다음 2개 퀘스트, 목표달성일 경우 랜덤 2개 퀘스트 보여주기
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # serializer = QuestListDetailSerializer(instance)
        serializer = QuestListDetailSerializer(
            instance,
            context={'user_id': request.user.id}
        )
        return Response(serializer.data)

    # url : /users/questlist/{pk}/start_quest (퀘스트 시작 todo->doing)
    @action(detail=True, methods=['get'])
    def start_quest(self, request, pk):
        quest = self.get_object()
        quest.state = 'DOING'
        quest.save()
        serializer = self.get_serializer(quest)
        return Response(serializer.data)

    # url : /users/questlist/{pk}/abandon_quest (퀘스트 포기 doing->abandon)
    @action(detail=True, methods=['get'])
    def abandon_quest(self, request, pk):
        quest = self.get_object()
        quest.state = 'ABANDON'
        quest.save()
        serializer = self.get_serializer(quest)
        return Response(serializer.data)

    # url : /users/questlist/{pk}/delete_quest (퀘스트 삭제 done->삭제)
    @action(detail=True, methods=['get'])
    def delete_quest(self, request, pk):
        quest = self.get_object()
        self.perform_destroy(quest)
        return Response(status=status.HTTP_202_ACCEPTED)

    # url : /users/questlist/{pk}/success_quest (퀘스트 완료 doing->done)
    @action(detail=True, methods=['get'])
    def success_quest(self, request, pk):
        quest = self.get_object()
        quest.state = 'DONE'
        quest.save()

        # TODO: 유저 정보 갱신 필요 !!! (퀘스트 완료했으니까 level?)

        serializer = self.get_serializer(quest)
        return Response(serializer.data)


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


# 모든 quest를 유저에 할당 (유저별 1번만 호출, questlist에 "todo"인 상태로) ----------> 어느 타이밍에 할 것인지 아직..?
@api_view(['GET'])
def quest_to_user(request):
    '''
            모든 quest를 user에게 할당 (user별 1번만 호출, default state:"todo")
            ---
    '''
    # QuestList.objects.all().delete()
    uid = request.user
    all_quest = Quest.objects.all()
    for quest in all_quest:
        QuestList.objects.create(uid=uid, qid=quest)
    return Response(status=status.HTTP_201_CREATED)
