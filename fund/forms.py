from django import forms
from django.utils.timezone import now
from fund import models


class FundForm(forms.ModelForm):

    class Meta:
        model = models.Fund
        fields = '__all__'
        exclude = ('owner', 'pub_date', )


class ExpenseForm(forms.ModelForm):

    class Meta:
        model = models.Expense
        fields = '__all__'
        exclude = ('fund',)
