from django.shortcuts import render, redirect
from LMS.models import Profile, Notification

# Views are here
def home(request):
    context = {
        "title": 'خانه',
        "subtitle": "به مدرسه شهدای فرهنگی خوش آمدید",
        "active": "home",
    }
    if request.user.is_authenticated:
        if not request.user.is_superuser:
            notifications = []
            for notification_public in Notification.objects.filter(to='همه کاربران'):
                notifications.append(notification_public)
            if Profile.objects.filter(user=request.user)[0].role == "Student":
                for notif in Notification.objects.filter(to='همه دانش آموزان'):
                    notifications.append(notif)
            else:
                for notif in Notification.objects.filter(to='همه معلمان'):
                    notifications.append(notif)
            context['notifications'] = notifications
    return render(request, 'home.html', context)