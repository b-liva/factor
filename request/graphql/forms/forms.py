from django.forms import ModelForm
from graphql_relay import from_global_id

from request.models import Requests, ReqSpec, Xpref, PrefSpec, Payment
from accounts.models import User


# Request Mutations
class RequestModelForm(ModelForm):

    class Meta:
        model = Requests
        # fields = '__all__'
        exclude = ('pub_date', 'is_active',)


class ReqSpecModelForm(ModelForm):

    class Meta:
        model = ReqSpec
        # fields = '__all__'
        exclude = ('is_active',)


# Proforma forms
class ProformaModelForm(ModelForm):
    def __init__(self, data=None, *args, **kwargs):
        current_user = User.objects.get(pk=4)
        attrs = ['req_id']
        # Changing graphql ids to pk
        if data is not None:
            data['owner'] = str(current_user.pk)
            for attr in attrs:
                if attr in data:
                    data[attr] = from_global_id(data[attr])[1]
            last = Xpref.objects.order_by('number').last()
            data['number'] = last.number + 1
        super(ProformaModelForm, self).__init__(data, args, kwargs)

    class Meta:
        model = Xpref
        # fields = '__all__'
        exclude = ('is_active', 'pub_date',)


class PrefSpecForm(ModelForm):
    class Meta:
        model = PrefSpec
        fields = '__all__'


# Payment forms
class PaymentModelForm(ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
