from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view, action
from .serializers import UserSerializer,FeedSerializer,QuestListSerializer
from .models import CustomUser,Feed,QuestList
from rest_framework.response import Response
import datetime
from django.db import IntegrityError


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
        user_info  = self.get_object()
        user_info.nickname = nickname 

        try:
            self.perform_update(user_info) 
            return Response(status=status.HTTP_201_CREATED)
        except IntegrityError: 
            # 이미 존재하는 닉네임일때
            return Response(status=status.HTTP_409_CONFLICT) 
        

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
    serializer.level_save(user_info)
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