from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=80, label="ایمیل", required=False)

class NotifcationForm(forms.ModelForm):
    class Meta():
        model = Notification
        fields = ('to', 'message')
        labels = {
            'to': 'برای',
            'message': 'پیام',
        }