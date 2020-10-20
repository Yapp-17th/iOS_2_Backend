from rest_framework import viewsets
from rest_framework.response import Response

from planets.models import Planet
from users.models import CustomUser as User
from planets.serializers import PlanetSerializer


class PlanetViewSet(viewsets.ModelViewSet):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer

    def list(self, request, *args, **kwargs):
        # 현재 로그인한 유저가 속한 행성의 유저들을 보여줌
        user = User.objects.get(id=self.request.user.id)
        my_planet = Planet.objects.filter(id=user.planet_id).first()
        if not my_planet:
            raise ValueError('유저가 아직 행성에 참여하지 않았음')

        serializer = self.get_serializer(my_planet)
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

        serializer = self.get_serializer(cur_planet)
        return Response(serializer.data)
