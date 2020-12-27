from math import ceil

from planets.models import Planet
from users.models import CustomUser
from users.push_fcm_notification import send_to_challenge

def create_planet():
    # 모든 유저 할당 가능한 수의 행성 생성, 유저의 status 고려해야할까?
    user_cnt = CustomUser.objects.count()
    for _ in range(ceil(user_cnt / 10)):
        Planet.objects.create()
    users = CustomUser.objects.all()
    for user in users:
        send_to_challenge(user.registration_token)



def delete_planet():
    queryset = Planet.objects.all()
    queryset.delete()
