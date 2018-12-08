from django import forms
from django.contrib.auth.models import User
from django.core import validators
from customer import models
from customer.models import Type


class CustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['type'].queryset = Type.objects.all()
        self.fields['type'].label_from_instance = lambda obj: "%s" % obj.name

    class Meta:
        model = models.Customer
        fields = '__all__'
        exclude = ('pub_date', 'owner', 'representator')
        widgets = {
            'pub_date': forms.DateInput(attrs={
                'class': 'datetime-input form-control',
                'id': 'pub_datePicker'
            }),
            'code': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Code here',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام مشتری',

            }),
            'date2': forms.DateInput(attrs={
                'class': 'form-control',
            }),
            'type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'fax': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'addr': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            # 'agent': forms.Select(attrs={
            #     'class': 'form-control',
            # }),
        }
        labels = {
            'code': ('کد'),
            'name': ('نام'),
            'date2': ('تاریخ'),
            'type': ('دسته بندی'),
            'phone': ('تلفن'),
            'fax': ('فکس'),
            'postal_code': ('کد پستی'),
            'addr': ('آدرس'),
            'agent': ('نماینده'),
        }

        # types = forms.ModelChoiceField(queryset=Type.objects.filter(), label='room', widget=forms.Select)


class AddressForm(forms.ModelForm):

    class Meta:
        model = models.Address
        fields = '__all__'
        exclude = ('customer', 'name')
        widgets = {
            'fax': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'postal_code': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'fax': ('فکس'),
            'postal_code': ('کد پستی'),
            'address': ('آدرس'),
        }


class PhoneForm(forms.ModelForm):

    class Meta:
        model = models.Phone

        fields = '__all__'
        exclude = ('add',)
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'phone_number': ('شماره تلفن'),
        }