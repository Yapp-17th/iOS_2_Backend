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

        # 정렬 기준 : "일주일간"의 플로깅 횟수->거리->시간
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
        if user.planet:
            raise ValueError('이번주는 이미 행성에 참여했음')
        # 속한 유저 수가 10보다 작으면서 id 가장 작은 행성(first)
        cur_planet = Planet.objects.filter(user_cnt__lt=10).first()
        cur_planet.user_cnt += 1
        cur_planet.save()
        user.planet = cur_planet
        user.save()

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
