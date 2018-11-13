from django import forms
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
        model = models.PaymentFiles
        fields = '__all__'
        exclude = ('pay',)
        widgets = {"image": forms.FileInput(attrs={'multiple': True})}
