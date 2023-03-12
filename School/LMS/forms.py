from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from .models import *
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from . import password_validation

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(label='پست الکترونیکی')
    error_messages = {
        "password_mismatch": _("رمز عبور با تکرارش مطابقت ندارد"),
    }
    password1 = forms.CharField(
        label=_("رمز عبور"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    password2 = forms.CharField(
        label=_("تایید رمز عبور"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("رمز عبور قبل را وارد کنید برای تایید شدن."),
    )
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")
        labels = {
            'username': _('نام کاربری'),
            'first_name': _('نام'),
            'last_name': _('نام خانوادگی'),
        }
        field_classes = {"username": UsernameField, "first_name": forms.CharField, "last_name": forms.CharField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
                "autofocus"
            ] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        print(user)
        if commit:
            user.save()
        return user
class NotifcationForm(forms.ModelForm):
    class Meta():
        model = Notification
        fields = ('to', 'message')
        labels = {
            'to': 'برای',
            'message': 'پیام',
        }

class SampleExamForm(forms.ModelForm):
    class Meta:
        model = SampleExam
        fields = ('subject', 'grade', 'file')
        labels = {
            'subject': 'نام درس',
            'grade': 'پایه',
            'file': 'فایل'
        }
