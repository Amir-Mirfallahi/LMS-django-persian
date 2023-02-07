from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from LMS.models import Profile
from .forms import LoginForm

# Create your views here.
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.GET.get("next") or "/")
    else:
        form = LoginForm(request)
    
    return render(request, 'accounts/login.html', {"form": form})
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('/login')
    return render(request, 'accounts/logout.html', {"title": 'خروج از حساب'})
def account(request):
    if Profile.objects.filter(user=request.user):
        role = Profile.objects.filter(user=request.user)[0].role
    else:
        role = "superuser"
    return render(request, 'accounts/account.html', {"title": 'حساب کاربری', "role": role})
