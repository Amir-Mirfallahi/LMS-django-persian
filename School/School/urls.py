from django.contrib import admin
from django.urls import path, include
from accounts.views import (
    login_view,
    logout_view,
    account,
)
from .views import (
    home,
    retreive_post,
    about_us,
    contact_us,
    search,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path("login/", login_view),
    path('logout/', logout_view),
    path('posts/<str:slug>', retreive_post),
    path('search/', search),
    path('account/', account),
    path('about-us', about_us),
    path('contact-us', contact_us),
    path('account/', include('LMS.urls'))
]
