from django import forms
from incomes.models import Income, IncomeRow


class IncomeModelForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = '__all__'


class IncomeRowModelForm(forms.ModelForm):
    class Meta:
        model = IncomeRow
        fields = '__all__'
