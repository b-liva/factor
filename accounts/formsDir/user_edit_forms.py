from django.forms import (ModelForm, forms)
from accounts.models import User
from customer.models import Customer


class AccountUpdateForm(ModelForm):

    class Meta:
        model = User

        fields = ('first_name', 'last_name')

        labels = {
            'username': 'نام کاربری',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
        }


class CustomerProfileUpdateForm(ModelForm):

    class Meta:
        model = Customer

        fields = ('name', 'phone', 'fax', 'postal_code', 'addr', )

        labels = {
            'name': 'شرکت',
            'phone': 'تلفن',
            'fax': 'فکس',
            'postal_code': 'کد پستی',
            'addr': 'آدرس',
        }

