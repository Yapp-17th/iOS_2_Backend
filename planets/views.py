from datetime import datetime

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response

from planets.models import Planet
from users.models import CustomUser as User, Feed
from planets.serializers import PlanetSerializer
from users.serializers import UserSerializer


class PlanetViewSet(viewsets.ModelViewSet):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer

    def list(self, request, *args, **kwargs):
        # 현재 로그인한 유저가 속한 행성의 유저들을 보여줌
        user = User.objects.get(id=self.request.user.id)
        my_planet = Planet.objects.filter(id=user.planet_id).first()
        if not my_planet:
            raise ValueError('유저가 아직 행성에 참여하지 않았음')
        user_in_planet = my_planet.customuser_set.all()

        # 일주일 간의 플로깅 횟수 기준으로 정렬
        # week_feed = Feed.objects.filter(date__range=[my_planet.start_date, my_planet.end_date])
        # for uip in user_in_planet:
        #     feed_cnt = week_feed.filter(uid=uip.id).count()
        # planet_ranking = user_in_planet.extra(select={'week_feed_cnt': '정렬 기준 함수'}).order_by('week_feed_cnt')
        # print("# user in planet : ", user_in_planet)
        # print("# user ranking in planet : ", planet_ranking)

        # serializer = self.get_serializer(user_in_planet, many=True)
        serializer = UserSerializer(user_in_planet, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = User.objects.get(id=self.request.user.id)


        cur_planet = Planet.objects.last()       # 가장 마지막에 생성한 행성 가져옴
        print("# last_planet : ", cur_planet)
        if cur_planet and cur_planet.customuser_set.count() < 10:
            # 유저의 planet 필드에 현재 행성 넣어주기
            user.planet = cur_planet
            user.save()
            print("# my_planet : ", cur_planet)
        else:
            # 새로운 행성 만들어서 넣어주기
            new_planet = Planet.objects.create()
            user.planet = new_planet
            user.save()
            print("# my_planet : ", new_planet)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
