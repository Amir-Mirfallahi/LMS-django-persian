from django.shortcuts import render, redirect
from LMS.models import Profile, Notification, Post

# Views are here
def home(request):
    context = {
        "title": 'خانه',
        "subtitle": "به مدرسه شهدای فرهنگی خوش آمدید",
        'posts': Post.objects.all()
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

def retreive_post(request, slug):
    context = {
        'title': 'نوشته',
        'posts': Post.objects.all(),
        'post': Post.objects.get(slug=slug),
        'uploaded_time': Post.objects.get(slug=slug).uploaded_time[:11],
    }
    return render(request, 'post.html', context)

def about_us(request):
    context = {
        'title': 'درباره ما',
        'posts': Post.objects.all()
    }
    return render(request, 'about-us.html', context)
def contact_us(request):
    context = {
        'title': 'تماس با ما',
        'posts': Post.objects.all()
    }
    return render(request, 'contact-us.html', context)

def search(request):
    s = request.GET.get('s')
    related_post_title = Post.objects.filter(title__contains=s)
    related_post_content = Post.objects.filter(content__contains=s)
    context = {
        'title': 'جست و جو',
        'related_post_title': related_post_title,
        'realated_post_content': related_post_content,
        'posts': Post.objects.all()
    }
    return render(request, 'search.html', context)