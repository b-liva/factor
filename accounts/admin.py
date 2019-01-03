from django.contrib import admin
# from django.contrib.auth.models import User as DefaultUser
from accounts.models import User
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

admin.site.register(User, CustomUserAdmin)

from django.contrib.auth.models import Group
# Register your models here.

# admin.site.unregister(DefaultUser)
# admin.site.register(User)
# admin.site.unregister(Group)