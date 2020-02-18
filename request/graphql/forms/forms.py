from django.forms import ModelForm

from request.models import Requests, ReqSpec, Xpref, PrefSpec, Payment


# Request Mutations
class RequestModelForm(ModelForm):
    class Meta:
        model = Requests
        fields = '__all__'


class ReqSpecModelForm(ModelForm):
    class Meta:
        model = ReqSpec
        fields = '__all__'


# Proforma forms
class ProformaModelForm(ModelForm):
    class Meta:
        model = Xpref
        fields = '__all__'


class PrefSpecForm(ModelForm):
    class Meta:
        model = PrefSpec
        fields = '__all__'


# Payment forms
class PaymentModelForm(ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
