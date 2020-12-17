from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from quests.models import Quest
from planets.models import Planet
from .serializers import UserSerializer, FeedSerializer, QuestListSerializer, QuestListDetailSerializer
from .models import CustomUser,Feed,QuestList
from rest_framework.response import Response
import datetime


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get','delete','head']
    
    # def update(self, request, *args, **kwargs):
    #     '''
    #             user 가입시 닉네임 등록
    #             ---
    #             (토큰 필요)
    #             user가 등록된 후 닉네임을 PUT 요청을 통해
    #             유저정보에 추가적으로 등록합니다.
    #             성공적으로 실행되면 201 응답을 리턴하며
    #             닉네임이 중복값일경우 409 응답을 리턴합니다.
    #
    #     '''
    #     nickname = request.data.get('nickname')
    #     if nickname == "":
    #         return Response(status=status.HTTP_409_CONFLICT)
    #     users = CustomUser.objects.all()
    #     for user in users:
    #         if user.nickname == nickname:
    #             return Response(status=status.HTTP_409_CONFLICT)
    #
    #     user_info  = self.get_object()
    #     user_info.nickname = nickname
    #     self.perform_update(user_info)
    #     return Response(user_info,status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        '''
                탈퇴하기
                ---
                (토큰 필요)
                유저 정보가 사라지고 유저와 관련된 데이터들이 삭제됩니다.
        '''
        user_info = self.get_object()
        if user_info.planet:
            my_planet = Planet.objects.get(id=user_info.planet.id)
            my_planet.user_cnt -= 1
            my_planet.save()

        self.perform_destroy(user_info)
        return Response(status=status.HTTP_202_ACCEPTED)
        

    #lastlogined 갱신(앱실행시 호출)
    @action(detail=True, methods=['get'])
    def update_lastlogined(self, request, pk, *args, **kwargs):
        '''
                어플 실행시 최근 로그인 시간 , 상태값 갱신
                ---
                (토큰 필요)
                어플 실행할떄마다 lastlogined 필드값을 현재시간으로 갱신합니다.
                또한 유저의 활동상태를 Normal로 변경합니다.
                성공적으로 실행되면 201 응답을 리턴합니다.
        '''
        user_info = self.get_object()
        user_info.lastlogined = datetime.datetime.now()
        user_info.state = "N"
        self.perform_update(user_info)
        return Response(user_info,status=status.HTTP_201_CREATED)
    

class FeedViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    http_method_names = ['get','post','delete','head']

    def list(self,request):
        '''
                피드 리스트 출력
                (토큰 필요)
                ---
                request 한 유저가 작성한 피드를 보여줍니다.
        '''
        queryset = Feed.objects.filter(uid=request.user.id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
 
    def create(self,request):
        '''
                피드 등록 및 경험치 증가
                (토큰 필요)
                ---
                피드 등록시 등록한 유저의 경험치가 1 증가되면서
                사진, 거리, 시간등 Feed내의 필드값들이 저장됩니다.
        '''
        serializer = self.get_serializer(data=request.data)
        #피드 등록시 경험치 1증가
        user = CustomUser.objects.get(id=request.data.get(
            'uid',''
        ))
        user.experience += 1
        user.save()
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = CustomUser.objects.get(id=instance.uid.id)
        user.experience -= 1
        user.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)    
    
    #신고기능_피드
    @action(detail=True, methods=['get'])
    def report_feed(self,request, pk, *args, **kwargs):
        '''
            피드 신고 (3회이상시 피드 삭제)
            ---
            (토큰 필요)
            신고회원 id값 저장 후 신고수를 누적시킵니다.
            동일한 회원이 신고할 시 400 응답을 리턴하고
            해당 신고는 반영되지 않습니다.
            신고자가 3명이상이면 피드를 삭제하면서 경험치를 줄입니다.(음수O) 
            피드 삭제시 202 응답을 리턴합니다.
        '''
        feed_info = self.get_object()
        report_user = CustomUser.objects.get(id=request.user.id)  
        #중복방지
        if str(report_user.id) not in feed_info.report_uidList: 
            feed_info.report_uidList.append(report_user.id)
            self.perform_update(feed_info)
            
            #3번째 신고면 삭제
            if len(feed_info.report_uidList) >= 3: 
                user = CustomUser.objects.get(email = feed_info.uid)
                user.experience -= 1
                user.save()
                self.perform_destroy(feed_info)
            return Response(status = status.HTTP_202_ACCEPTED)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'],url_path='others_feed', url_name='others_feed')
    def others_feed(self,request):
        '''
                    타 유저 피드 리스트 출력
                    (토큰 필요)
                    ---
                    id값을 json 으로 보내면 해당 id값을 가진 유저의 피드를 보여줍니다.
        '''
        serializer = self.get_serializer(data=request.data)
        queryset = Feed.objects.filter(uid=request.data.get("id"))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        

class QuestListViewSet(viewsets.ModelViewSet):
    queryset = QuestList.objects.all()
    serializer_class = QuestListSerializer
    http_method_names = ['get', 'head']

    def list(self, request, *args, **kwargs):
        queryset = QuestList.objects.filter(uid=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # 퀘스트 상세 설명 화면, 학습퀘스트일 경우 다음 2개 퀘스트, 목표달성일 경우 랜덤 2개 퀘스트 보여주기
    def retrieve(self, request, pk):
        '''
            퀘스트 상세 설명 화면
            ---
            (토큰 필요)
            선택한 퀘스트의 정보와 학습퀘스트일 경우 다음 step 퀘스트 2개, 목표달성일 경우 랜덤 2개 퀘스트를 함께 보여줍니다.
            more quest의 경우, 각 유저가 아직 수행하지 않은 퀘스트들을 보여주며 2개 미만일 경우 0개 또는 1개의 퀘스트를 반환할 수 있습니다.
        '''
        instance = QuestList.objects.get(uid=request.user, qid_id=pk)
        serializer = QuestListDetailSerializer(
            instance,
            context={'user_id': request.user.id}
        )
        return Response(serializer.data)

    # url : /users/questlist/{pk}/start (퀘스트 시작 todo->doing)
    @action(detail=True, methods=['get'])
    def start(self, request, pk):
        '''
                퀘스트 시작
                ---
                (토큰 필요)
                선택한 퀘스트를 "시작" 처리합니다. (todo->doing)
                성공적으로 실행되면 200 응답을 리턴합니다.
        '''
        quest = QuestList.objects.get(uid=request.user, qid_id=pk)
        quest.state = 'DOING'
        quest.save()
        return Response(status=status.HTTP_200_OK)

    # url : /users/questlist/{pk}/abandon (퀘스트 포기 doing->todo)
    @action(detail=True, methods=['get'])
    def abandon(self, request, pk):
        '''
                퀘스트 포기
                ---
                (토큰 필요)
                선택한 퀘스트가 학습퀘스트일 경우 학습퀘스트 전체 포기 (전체 삭제)
                선택한 퀘스트가 목표달성 퀘스트일 경우 선택한 목표달성 퀘스트만 포기 (준비 탭으로)
                성공적으로 실행되면 200 응답을 리턴합니다.
        '''
        quest = QuestList.objects.get(uid=request.user, qid_id=pk)
        if quest.qid.category == 'T':
            # 트레이닝 퀘스트 포기는 전체 포기
            QuestList.objects.filter(uid=request.user, qid__category='T').delete()
            return Response(status=status.HTTP_200_OK)
        elif quest.qid.category == 'R':
            quest.state = 'TODO'
            quest.save()
            return Response(status=status.HTTP_200_OK)

    # url : /users/questlist/{pk}/delete (퀘스트 삭제 done->삭제)
    @action(detail=True, methods=['get'])
    def delete(self, request, pk):
        '''
                퀘스트 삭제
                ---
                (토큰 필요)
                선택한 완료 상태인 퀘스트를 삭제합니다.
                성공적으로 실행되면 200 응답을 리턴합니다.
        '''
        quest = QuestList.objects.get(uid=request.user, qid_id=pk)
        self.perform_destroy(quest)
        return Response(status=status.HTTP_200_OK)

    # url : /users/questlist/{pk}/success (퀘스트 완료 doing->done)
    @action(detail=True, methods=['get'])
    def success(self, request, pk):
        '''
                퀘스트 완료
                ---
                (토큰 필요)
                선택한 퀘스트를 "완료"상태로 바꾸고 유저정보 갱신합니다. (experience += 1.5)
                성공적으로 실행되면 200 응답을 리턴합니다.
        '''
        quest = QuestList.objects.get(uid=request.user, qid_id=pk)
        quest.state = 'DONE'
        quest.save()
        # 유저 경험치 +1.5
        quser = CustomUser.objects.get(id=request.user.id)
        quser.experience += 1.5
        quser.save()
        return Response(status=status.HTTP_200_OK)


#랭크 업데이트 (report_feed 실행후, 새로고침 실행후 호출)
@api_view(['GET'])
def rank_update(request):
    '''
            랭크 업데이트
            ---
            (토큰 필요)
            전체유저 순위를 정렬하여 랭크값을 갱신합니다.
            갱신이 완료되면 202 응답을 리턴합니다.

    '''
    user_info = CustomUser.objects.all()
    serializer = UserSerializer(user_info)
    serializer.rank_save(user_info)
    return Response(status = status.HTTP_202_ACCEPTED)

#레벨 업데이트(새로고침 실행후 호출)
@api_view(['GET'])
def level_update(request, *args, **kwargs):
    '''
            레벨 업데이트
            ---
            (토큰 필요)
            유저의 경험치가 5 이상일경우 경험치/5의 몫만큼 레벨을 올립니다.
            레벨이 올라가면 경험치는 경험치/5의 나머지로 변경됩니다.
            성공적으로 갱신이 완료되면 202 응답을 리턴합니다.
    '''
    serializer_context = {
        'request': request,
    }
    user_info = CustomUser.objects.get(id = request.user.id)
    serializer = UserSerializer(user_info, context=serializer_context)
    serializer.level_save(user_info)
    return Response(serializer.data,status = status.HTTP_202_ACCEPTED)


# 모든 quest를 유저에 할당 (유저별 1번만 호출, questlist에 "todo"인 상태로)
@api_view(['GET'])
def quest_to_user(request):
    '''
            모든 quest를 user에게 할당
            ---
            (토큰 필요)
            회원가입한 후, 유저에게 퀘스트를 부여하기 위한 것
            (user별 1번만 호출, default state:"todo")
            성공적으로 실행되면 200 응답을 리턴합니다.
    '''
    uid = request.user
    QuestList.objects.filter(uid=uid).delete()

    all_quest = Quest.objects.all()
    for quest in all_quest:
        QuestList.objects.create(uid=uid, qid=quest)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def see_others_feed(request,self):
    '''
                피드 리스트 출력
                (토큰 필요)
                ---
                request 한 유저가 작성한 피드를 보여줍니다.
    '''
    queryset = Feed.objects.filter(uid=request.data.get("id"))
    page = self.paginate_queryset(queryset)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    serializer = self.get_serializer(queryset, many=True)
    return Response(serializer.data)
