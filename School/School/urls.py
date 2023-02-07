from django.contrib import admin
from django.urls import path, include
from accounts.views import (
    login_view,
    logout_view,
    account,
)
from .views import (
    home
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path("login/", login_view),
    path('logout/', logout_view),
    path('account/', account),
    path('account/', include('LMS.urls'))
]
