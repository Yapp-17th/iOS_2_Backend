from rest_framework import serializers
from users.models import CustomUser,Feed,QuestList

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'nickname', 'level', 'rank', 'state', 'planet', 'weekly_stats', 'monthly_stats']
    
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


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = '__all__'

class QuestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestList
        fields= '__all__'