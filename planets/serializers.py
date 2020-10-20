from rest_framework.fields import SerializerMethodField

from planets.models import Planet
from rest_framework import serializers

from users.serializers import UserSerializer


class PlanetSerializer(serializers.ModelSerializer):
    players = SerializerMethodField()

    class Meta:
        model = Planet
        fields = ('start_date', 'end_date', 'user_cnt', 'players')

    def get_players(self, instance):
        # 정렬 기준 : "일주일간"의 플로깅 횟수->거리->시간
        players = sorted(instance.players.all(),
                         key=lambda p: (p.get_feed_cnt(instance), p.get_distance(instance) or 0, p.get_time(instance) or 0),
                         reverse=True)
        return UserSerializer(players, many=True).data
