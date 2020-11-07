from users import views
from users.models import CustomUser,Feed
import datetime
from push_notifications.models import APNSDevice

from dateutil.relativedelta import relativedelta

def check_dormant():
    users = CustomUser.objects.all()
    for user in users:
        if user.state == "N":
            if datetime.datetime.now() >= user.lastlogined + datetime.timedelta(minutes=1):
                user.state = "D"
                #push noti
                #device = GCMDevice.objects.get(registration_id=gcm_reg_id)
                #device.send_message("Test")
                user.save()


def monthly_stats():
    users = CustomUser.objects.all()
    startday = datetime.datetime.now() - relativedelta(months=1)
    endday = datetime.datetime.now()
    for user in users:
        feeds = Feed.objects.filter(uid=user.id ,date__range=[startday,endday])
        feeds_count = feeds.count()
        month = endday.month - user.registeredDate.month
        avg_count = round(feeds_count/month,2)
        user.monthly_stats = avg_count
        user.save()
    
