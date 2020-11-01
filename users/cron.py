from users import views
from users.models import CustomUser
import datetime

def check_dormant():
    users = CustomUser.objects.all()
    for user in users:
        if user.state == "N":
            if datetime.datetime.now() >= user.lastlogined + datetime.timedelta(days=3):
                user.state = "D"
                user.save()