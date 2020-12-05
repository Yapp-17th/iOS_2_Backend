from math import ceil

from planets.models import Planet
from users.models import CustomUser


def create_planet():
    # 모든 유저 할당 가능한 수의 행성 생성, 유저의 status 고려해야할까?
    user_cnt = CustomUser.objects.count()
    for _ in range(ceil(user_cnt / 10)):
        Planet.objects.create()
        #device = APNSDevice.objects.get(registration_id=apns_token)
        #device.send_message(message = {"title" : "행성생성","body" : "참여하세요!"})


def delete_planet():
    queryset = Planet.objects.all()
    queryset.delete()
