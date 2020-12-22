from users import views
from users.models import CustomUser,Feed
import datetime
from push_notifications.models import APNSDevice
from dateutil.relativedelta import relativedelta

def check_3days():
    users = CustomUser.objects.all()
    for user in users:
        if user.state == "N":
            if datetime.datetime.now() >= user.lastlogined + datetime.timedelta(days=3):
                user.state = "D"
                user.save()

#def check_7days():
    #users = CustomUser.objects.filter(state = "D")
    #for user in users:
    #    if datetime.datetime.now() >= user.lastlogined + datetime.timedelta(days=7): 
        #device = APNSDevice.objects.get(registration_id=apns_token)
        #device.send_message(message = {"title" : "3일 접속X","body" : "들어오세요!"})
 
def monthly_stats():
    users = CustomUser.objects.all()
    startday = datetime.datetime.now() - relativedelta(months=1)
    endday = datetime.datetime.now()
    for user in users:
        feeds = Feed.objects.filter(uid=user.id ,date__range=[startday,endday])
        feeds_count = feeds.count()
        month = endday.month - user.registeredDate.month
        if month == 0:
            user.save()
        else:
            avg_count = round(feeds_count/month,2)
            user.monthly_stats = avg_count
            user.save()

def weekly_stats():
    week = ['월','화','수','목','금','토','일']
    startday = datetime.datetime.now() - datetime.timedelta(weeks=1)
    endday = datetime.datetime.now()
    print(startday,endday)
    all_users = list(CustomUser.objects.all().values_list('id',flat=True))
    feeds = Feed.objects.filter(date__range=[startday,endday]).values_list('uid',flat=True).distinct()
    for i in feeds:
        user = CustomUser.objects.get(id = int(i))
        best = Feed.objects.filter(date__range=[startday,endday],uid = int(i)).order_by('-time')[0]
        print(Feed.objects.filter(date__range=[startday,endday],uid = int(i)).order_by('-time')[0])
        all_users.remove(i)
        user.weekly_stats = week[best.date.weekday()]
        user.save()
    print(all_users)
    for j in all_users:
        user = CustomUser.objects.get(id = int(j))
        user.weekly_stats = '-'
        user.save()
