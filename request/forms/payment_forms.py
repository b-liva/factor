from django import forms
from request import models


class PaymentFrom(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PaymentFrom, self).__init__(*args, **kwargs)
        # list = [ 'images']
        list = []
        for visible in self.visible_fields():
            if visible.name not in list:
                visible.field.widget.attrs['class'] = 'form-control'

        self.fields['xpref_id'].queryset = self.fields['xpref_id'].queryset.order_by('number')

    class Meta:
        model = models.Payment
        fields = '__all__'
        exclude = (
            'owner',
            'payment_date',
            'customer',
            'is_active',
            'temp_number',
        )
        widgets = {
            'date_fa': forms.DateInput(attrs={
                'id': 'date_fa'
            })
        }

        labels = {
            'xpref_id': 'شماره پیشفاکتور',
            'number': 'شماره پرداخت',
            'date_fa': 'تاریخ پرداخت',
            'amount': 'مبلغ',
            'summary': 'شرح',
        }


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
        labels = {
            'image': 'آپلود تصاویر'
        }
