from django.contrib import admin
# from django.contrib.auth.models import User as DefaultUser
from django.contrib.auth import get_user_model
from accounts.models import CustomerUser
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm, CustomerUserCreationForm, CustomerUserChangeForm

User = get_user_model()


class CustomUserAdmin(UserAdmin):
# class CustomUserAdmin(admin.ModelAdmin):
#     fieldsets = (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'is_customer')})
    # fields = ('is_customer', 'username', 'password',)
    model = User
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm


class CustomerUserAdmin(admin.ModelAdmin):
    # pass
    model = CustomerUser
    add_form = CustomerUserCreationForm
    form = CustomerUserChangeForm


admin.site.register(User, CustomUserAdmin)
# admin.site.register(User)
admin.site.register(CustomerUser, CustomerUserAdmin)

# Register your models here.

# admin.site.unregister(DefaultUser)
# admin.site.register(User)
# admin.site.unregister(Group)
