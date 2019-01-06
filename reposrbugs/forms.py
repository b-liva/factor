from django import forms
from reposrbugs.models import Bugs
from accounts.models import User
from django.core import validators


class BugForm(forms.ModelForm):

    class Meta:
        model = Bugs
        fields = '__all__'
        # exclude = ('pub_date', 'owner', 'representator')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان',

            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'suggestion': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'title': ('عنوان'),
            'description': ('شرح'),
            'suggestion': ('پیشنهاد'),
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