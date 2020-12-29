from math import ceil

from planets.models import Planet
from users.models import CustomUser
from users.push_fcm_notification import send_to_push

def create_planet():
    # 모든 유저 할당 가능한 수의 행성 생성, 유저의 status 고려해야할까?
    user_cnt = CustomUser.objects.count()
    title='챌린지 행성이 갱신되었습니다.'
    body='앱에 접속해서 확인해주세요!'
    for _ in range(ceil(user_cnt / 10)):
        Planet.objects.create()
    users = CustomUser.objects.all()
    for user in users:
        send_to_push(user.registration_token,title,body)



def delete_planet():
    queryset = Planet.objects.all()
    queryset.delete()
