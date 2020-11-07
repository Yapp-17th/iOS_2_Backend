from rest_framework.fields import SerializerMethodField

from planets.models import Planet
from rest_framework import serializers

from users.serializers import PlayerSerializer


class PlanetSerializer(serializers.ModelSerializer):
    players = SerializerMethodField()

    class Meta:
        model = Planet
        fields = ('id', 'start_date', 'end_date', 'user_cnt', 'players')

    def get_players(self, instance):
        # 수정된 정렬 기준 : [1회:1000점,1km:100점(0.01km:1점),1분:1점]으로 산출한 점수 (같은 점수면 배치는 이름순, 순위는 같게)
        players = sorted(instance.players.all(),
                         key=lambda p: (p.get_feed_cnt(instance) * 1000 + p.get_distance(instance) * 100 + p.get_time(instance)),
                         reverse=True)
        return PlayerSerializer(players, many=True).data
