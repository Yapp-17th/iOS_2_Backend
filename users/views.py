from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view, action

from quests.models import Quest
from .serializers import UserSerializer, FeedSerializer, QuestListSerializer, QuestListDetailSerializer
from .models import CustomUser,Feed,QuestList
from rest_framework.response import Response
import datetime
from django.db import IntegrityError
from dateutil.relativedelta import relativedelta


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
    def update(self, request, *args, **kwargs):
        '''
                user 가입시 닉네임 등록
                ---
                user가 등록된 후 닉네임을 PUT 요청을 통해
                유저정보에 추가적으로 등록합니다.
                성공적으로 실행되면 201 응답을 리턴하며
                닉네임이 중복값일경우 409 응답을 리턴합니다.
        ''' 
        nickname = request.data.get('nickname') 
        users = CustomUser.objects.all()
        for user in users:
            if user.nickname == nickname:
                return Response(status=status.HTTP_409_CONFLICT)
 
        user_info  = self.get_object()
        user_info.nickname = nickname 
        self.perform_update(user_info) 
        return Response(status=status.HTTP_201_CREATED)
        

    #lastlogined 갱신(앱실행시 호출)
    @action(detail=True, methods=['get'])
    def update_lastlogined(self, request, pk, *args, **kwargs):
        '''
                어플 실행시 최근 로그인 시간 , 상태값 갱신
                ---
                어플 실행할떄마다 lastlogined 필드값을 현재시간으로 갱신합니다.
                또한 유저의 활동상태를 Normal로 변경합니다.
                성공적으로 실행되면 201 응답을 리턴합니다.
        '''
        user_info = self.get_object()
        user_info.lastlogined = datetime.datetime.now()
        user_info.state = "N"
        self.perform_update(user_info)
        return Response(status=status.HTTP_201_CREATED)
    


class FeedViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer

    #신고기능_피드
    @action(detail=True, methods=['get'])
    def report_feed(self,request, pk, *args, **kwargs):
        '''
            피드 신고 (3회이상시 피드 삭제)
            ---
            신고회원 id값 저장 후 신고수를 누적시킵니다.
            동일한 회원이 신고할 시 400 응답을 리턴하고
            해당 신고는 반영되지 않습니다.
            신고자가 3명이상이면 피드를 삭제합니다. 
            피드 삭제시 202 응답을 리턴합니다.
        '''
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
    def start(self, request, pk):
        quest = self.get_object()
        quest.state = 'DOING'
        quest.save()
        serializer = self.get_serializer(quest)
        return Response(serializer.data)

    # url : /users/questlist/{pk}/abandon_quest (퀘스트 포기 doing->todo)
    @action(detail=True, methods=['get'])
    def abandon(self, request, pk):
        '''
                학습퀘스트 포기는 전체포기(전체 삭제) / 목표달성퀘스트 포기는 1개포기(준비 탭으로)
                ---
        '''
        quest = self.get_object()
        if quest.qid.category == 'T':
            # 트레이닝 퀘스트 포기는 전체 포기
            QuestList.objects.filter(uid=request.user, qid__category='T').delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        elif quest.qid.category == 'R':
            quest.state = 'TODO'
            quest.save()
            serializer = self.get_serializer(quest)
            return Response(serializer.data)

    # url : /users/questlist/{pk}/delete_quest (퀘스트 삭제 done->삭제)
    @action(detail=True, methods=['get'])
    def delete(self, request, pk):
        quest = self.get_object()
        self.perform_destroy(quest)
        return Response(status=status.HTTP_202_ACCEPTED)

    # url : /users/questlist/{pk}/success_quest (퀘스트 완료 doing->done)
    @action(detail=True, methods=['get'])
    def success(self, request, pk):
        quest = self.get_object()
        quest.state = 'DONE'
        quest.save()
        # 유저 경험치 +1.5
        quser = CustomUser.objects.get(id=request.user.id)
        quser.experience += 1.5
        quser.save()
        serializer = self.get_serializer(quest)
        return Response(serializer.data)


#랭크 업데이트 (report_feed 실행후, 새로고침 실행후 호출)
@api_view(['GET'])
def rank_update(request):
    '''
            랭크 업데이트
            ---
            전체유저 순위를 정렬하여 랭크값을 갱신합니다.
            갱신이 완료되면 202 응답을 리턴합니다.
    '''
    user_info = CustomUser.objects.all()
    serializer = UserSerializer(user_info)
    serializer.rank_save(user_info)
    return Response(status = status.HTTP_202_ACCEPTED)



#레벨 업데이트(새로고침 실행후 호출)
@api_view(['GET'])
def level_update(request,self, *args, **kwargs):
    '''
            레벨 업데이트
            ---
            전체유저 순위를 정렬하여 랭크값을 갱신합니다.
            갱신이 완료되면 202 응답을 리턴합니다.
    '''
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
