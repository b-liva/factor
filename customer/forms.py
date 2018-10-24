from django import forms
from django.core import validators
from customer import models
from customer.models import Type



class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = '__all__'
        types = forms.ModelChoiceField(queryset=Type.objects.filter(), label='room', widget=forms.Select)

