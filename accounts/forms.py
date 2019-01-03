from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from accounts import models
from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm



class EditProfileForm(UserChangeForm):
    class Meta:

        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password',
        )
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',

            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                # 'placeholder': 'Enter Title here',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',

            }),
        }
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'email': 'ایمیل',
        }


class PassChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(PassChangeForm, self).__init__(*args, **kwargs)
        # self.new_password1.label = 'new lable'

    class Meta:
        model = User
        fields = (
            'old_password',
            'new_password1',
            # 'new_password2',
        )
        widgets = {
            'old_password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'enter pass'

            }),
            'new_password1': forms.PasswordInput(attrs={
                'class': 'form-control',
            }),
            'new_password2': forms.PasswordInput(attrs={
                'class': 'form-control',
            }),
        }

        # labels = {
        #     'old_password': 'رمز قبلی',
        #     'new_password1': 'رمز جدید',
        #     'new_password2': 'تأیید رمز جدید',
        # }

    old_password = forms.CharField(
        label='رمز قدیم',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        # help_text=password_validation.password_validators_help_text_html(),
    )
    new_password1 = forms.CharField(
        label='رمز جدید',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        # help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='تکرار رمز',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
    )


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields
