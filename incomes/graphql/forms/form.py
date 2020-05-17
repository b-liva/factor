from django import forms
from graphql_relay import from_global_id

from incomes.models import Income, IncomeRow
from accounts.models import User


class IncomeModelForm(forms.ModelForm):
    def __init__(self, data=None, *args, **kwargs):
        print(data)
        current_user = User.objects.get(pk=4)
        attrs = ['customer', 'type']
        # Changing graphql ids to pk
        if data is not None:
            data['owner'] = str(current_user.pk)
            for attr in attrs:
                if attr in data:
                    data[attr] = from_global_id(data[attr])[1]
        super(IncomeModelForm, self).__init__(data, args, kwargs)

    class Meta:
        model = Income
        # fields = '__all__'
        exclude = ('is_active',)


class IncomeRowModelForm(forms.ModelForm):
    def __init__(self, data=None, *args, **kwargs):
        print(data)
        current_user = User.objects.get(pk=4)
        attrs = ['income', 'proforma']
        # Changing graphql ids to pk
        if data is not None:
            data['owner'] = str(current_user.pk)
            for attr in attrs:
                if attr in data:
                    data[attr] = from_global_id(data[attr])[1]
        super(IncomeRowModelForm, self).__init__(data, args, kwargs)

    class Meta:
        model = IncomeRow
        # fields = '__all__'
        exclude = ('is_active',)
