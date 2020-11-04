from rest_framework import serializers

from quests.models import Quest
from quests.serializers import QuestSerializer
from users.models import CustomUser,Feed,QuestList

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'nickname', 'level', 'rank', 'state', 'planet']
    
    def rank_save(self,user_info):
        rank_list = []
        #feed_count 갯수 기준으로 역순정렬
        for user in user_info:
            uid = user.id
            feed_count = len(Feed.objects.filter(uid=uid))
            rank_list.append([feed_count,uid])
        rank_list = sorted(rank_list, key = lambda x : -x[0])
        #feed_count를 rank값으로 변경 후 uid기준으로 정렬 
        user_idx = 0
        for rank in range(1,len(rank_list)+1):
            rank_list[user_idx][0] = rank
            user_idx+=1
        rank_list = sorted(rank_list, key = lambda x : x[1])
        
        user_idx = 0
        for user in user_info:
            user.rank = rank_list[user_idx][0]   
            user_idx += 1
            user.save()

    def level_save(self,user_info):
        #기준 정확하게 정해지면 추가
        user_info.level += 1
        user_info.save()


# 챌린지(행성)에서만 보여줄 user 정보(planet_score) 추가한 serializer 따로 정의
class PlayerSerializer(serializers.ModelSerializer):
    planet_score = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'nickname', 'planet_score']

    def get_planet_score(self, instance):
        return instance.get_feed_cnt(instance.planet) * 1000 \
               + instance.get_distance(instance.planet) * 100 \
               + instance.get_time(instance.planet)


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = '__all__'


class QuestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestList
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['qid'] = QuestSerializer(instance.qid).data
        return response


class QuestListDetailSerializer(serializers.ModelSerializer):
    more_quest = serializers.SerializerMethodField()

    class Meta:
        model = QuestList
        fields = ['id', 'uid', 'qid', 'state', 'more_quest']

    def get_more_quest(self, instance):
        queryset = QuestList.objects.filter(uid=self.context["user_id"], state="TODO")
        if instance.qid.category == "T":
            # training 이니까 다음 단계 퀘스트 2개 보여주기 (quest.category=="T" & questlist.uid==me & questlist.state=="todo")
            queryset = queryset.filter(qid__category="T")
        elif instance.qid.category == "R":
            # 목표달성형이니까 랜덤으로 퀘스트 2개 보여주기" (quest.category=="R" & questlist.state=="todo")
            queryset = queryset.filter(qid__category="R")
        return QuestListSerializer(queryset, many=True).data

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['qid'] = QuestSerializer(instance.qid).data
        return response
