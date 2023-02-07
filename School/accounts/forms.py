from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField

class LoginForm(AuthenticationForm):
    username = UsernameField(label='نام کاربری')
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)
