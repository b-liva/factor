from django import forms
from django.utils.timezone import now
from request import models


class PaymentFrom(forms.ModelForm):

    class Meta:
        model = models.Payment
        fields = '__all__'
        exclude = (
            'owner',
            'payment_date',
            'customer',
        )


class PaymentEditForm(forms.ModelForm):

    class Meta:
        model = models.Payment
        fields = '__all__'
        # exclude = ('req_id', 'owner', 'pub_date')
        widgets = {"image": forms.FileInput(attrs={'multiple': True})}


class PaymentFileForm(forms.ModelForm):

    class Meta:
        model = models.PaymentFiels
        fields = '__all__'
        # exclude = ('prof',)
        widgets = {"image": forms.FileInput(attrs={'multiple': True})}
