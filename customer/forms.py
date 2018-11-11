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
                'placeholder': 'Enter Name here',

            }),
            'date2': forms.DateInput(attrs={
                'class': 'form-control',
            }),
            'type': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'code': ('Code'),
            'date2': ('Date'),
            'type': ('Customer Type'),
        }
        

        # types = forms.ModelChoiceField(queryset=Type.objects.filter(), label='room', widget=forms.Select)



