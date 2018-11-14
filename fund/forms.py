from django import forms
from fund import models
# from crispy_forms.helper import FormHelper


class FundForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FundForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.Fund
        fields = '__all__'
        exclude = ('owner', 'pub_date', )

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Title here',

            }),
            'date_fa': forms.DateInput(attrs={
                'class': 'datetime-input form-control',
                'id': 'date_fa'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Summary Here...'
            })
        }
        labels = {
            'title': 'Title',
            'summary': 'Summary',
            'date_fa': 'Date',
        }


class ExpenseForm(forms.ModelForm):

    class Meta:
        model = models.Expense
        fields = '__all__'
        exclude = ('fund',)

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Title here',

            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Payment Amount'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Summary Here...'
            })
        }
        labels = {
            'title': 'Title',
            'summary': 'Summary',
            'amount': 'Amount',
        }
