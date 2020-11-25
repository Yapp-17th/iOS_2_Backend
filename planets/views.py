from rest_framework import viewsets, status
from rest_framework.response import Response

from planets.models import Planet
from users.models import CustomUser as User
from planets.serializers import PlanetSerializer

import datetime


class PlanetViewSet(viewsets.ModelViewSet):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    http_method_names = ['get', 'post', 'head']

    def list(self, request, *args, **kwargs):
        '''
                user가 속한 행성의 참여자들을 순위대로 보여줌
                ---
                (토큰 필요)
                챌린지 순위 : [1회:1000점, 1km:100점(0.01km:1점), 1분:1점]으로 산출한 점수
                성공적으로 실행되면 200 응답을 리턴하며
                유저가 아직 행성에 참여하지 않았다면 403 응답을 리턴합니다.
        '''
        user = User.objects.get(id=self.request.user.id)
        my_planet = Planet.objects.filter(id=user.planet_id).first()
        if not my_planet:
            return Response(status=status.HTTP_403_FORBIDDEN, data="아직 행성에 참여하지 않았음")

        serializer = self.get_serializer(my_planet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        '''
                이번주 행성(Planet)에 참여
                ---
                (토큰 필요)
                성공적으로 실행되면 200 응답을 리턴하며
                이번주에 이미 참여했다면 403 응답을 리턴합니다.
        '''
        user = User.objects.get(id=self.request.user.id)
        if user.planet:
            return Response(status=status.HTTP_403_FORBIDDEN, data="이번주 행성에 이미 참여했음.")
        # 속한 유저 수가 10보다 작으면서 id 가장 작은 행성(first)
        # cur_planet = Planet.objects.filter(user_cnt__lt=10).first()
        cur_planet = Planet(start_date=datetime.date.today(), end_date=datetime.date.today()+datetime.timedelta(days=4))
        if not cur_planet:
            pre_planet = Planet.objects.last()
            cur_planet = Planet(start_date=pre_planet.start_date, end_date=pre_planet.end_date)
        cur_planet.user_cnt += 1
        cur_planet.save()
        user.planet = cur_planet
        user.save()

        serializer = self.get_serializer(cur_planet)
        return Response(serializer.data, status=status.HTTP_200_OK)

