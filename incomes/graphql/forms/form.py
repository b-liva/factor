from django import forms
from incomes.models import Income, IncomeRow


class IncomeModelForm(forms.ModelForm):

    class Meta:
        model = Income
        exclude = ('is_active',)


class IncomeRowModelForm(forms.ModelForm):

    class Meta:
        model = IncomeRow
        exclude = ('is_active',)
