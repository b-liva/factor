from allauth import app_settings
from allauth.account.forms import (LoginForm as allauthLoginForm,
                                   SignupForm,
                                   ResetPasswordForm,
                                   ResetPasswordKeyForm,
                                   SetPasswordForm,
                                   ChangePasswordForm,
                                   PasswordField,
                                   SetPasswordField)
from allauth.account.views import LoginView
from django.contrib.auth import password_validation
# from django.contrib.auth.models import User
from accounts.models import User
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
        # fields = ('username', 'email')
        fields = '__all__'


class CustomUserCreationForm2(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        # fields = ('username', 'email')
        fields = ['email', 'password1', 'password2']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        # fields = UserChangeForm.Meta.fields
        fields = '__all__'


class CustomerUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email')


class CustomerUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='پسوورد', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    password2 = forms.CharField(label='تایید پسوورد', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ('username',)
        labels = {
            'username': 'نام کاربری'
        }

    def clean_passwrod2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('passwords dont match')
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_customer = True

        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='نام کاربری')
    password = forms.CharField(widget=forms.PasswordInput)


class CustomLoginForm(allauthLoginForm):

    # class Meta:
    #     labels = {
    #         'login': 'use',
    #         'password': 'pas',
    #     }

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        # here you can change the fields
        # self.fields['username'] = forms.EmailField(label='custom label')
        # self.fields['login'] = forms.CharField(label="نام کاربری")
        self.fields['login'] = forms.CharField(label="نام کاربری",
                                               widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['password'] = PasswordField(label="پسوورد")
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

        # self.fields['password'] = PasswordField(label="پسوورد")

    """
        this is also works but i used LOGIN_REDIRECT_URL  in settings
        def login(self, request, redirect_url=None):
            redirect_url = '/'
            return super(CustomLoginForm, self).login(request, redirect_url)
    
    """


class CustomSignForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'] = PasswordField(label='رمز عبور')
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

        self.fields['password2'] = PasswordField(label='تکرار رمز عبور')
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

        self.fields['username'] = forms.CharField(label="نام کاربری",
                                                  widget=forms.TextInput(attrs={'class': 'form-control'}))

        self.fields['email'] = forms.EmailField(label="ایمیل",
                                                widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def login(self, request, redirect_url=None):
        redirect_url = '/'
        return super(CustomSignForm, self).login(request, redirect_url)


class CustomerResetPasswordForm(ResetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(CustomerResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(
            label="ایمیل",
            required=True,
            widget=forms.TextInput(attrs={
                "type": "email",
                "size": "30",
                "placeholder": 'ایمیل',
                "class": 'form-control',
            })
        )


class CustomResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordKeyForm, self).__init__(*args, **kwargs)
        self.fields['password1'] = SetPasswordField(label='رمز عبور')
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

        self.fields['password2'] = PasswordField(label='تکرار رمز عبور')
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})


class CustomChangePasswordForm(ChangePasswordForm):

    def __init__(self, *args, **kwargs):
        super(CustomChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['oldpassword'] = PasswordField(label='رمز قبلی')
        self.fields['oldpassword'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

        self.fields['password1'] = SetPasswordField(label='رمز جدید')
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

        self.fields['password2'] = PasswordField(label='تکرار رمز جدید')
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

