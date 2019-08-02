from django import forms
from request import models
from django_jalali import forms as jforms


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


class PaymentSearchForm(forms.Form):
    customer = forms.CharField(label='مشتری', max_length=100, required=False)
    customer.widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'autocomplete'})
    date_min = jforms.jDateField(label='تاریخ(از)', required=False)
    date_min.widget = jforms.jDateInput(attrs={'id': 'date_fa_start', 'autocomplete': 'off', 'class': 'form-control', })
    date_max = jforms.jDateField(label='تاریخ(تا)', required=False)
    date_max.widget = jforms.jDateInput(attrs={
        'id': 'date_fa_end',
        'autocomplete': 'off',
        'class': 'form-control', })

    SORT_CHOICES = (
        # ('1', 'کیلووات',),
        # ('customer', 'مشتری',),
        ('date_fa', 'تاریخ',),
        ('number', 'شماره',),
        # ('4', 'تعداد',),
    )

    sort_asc_dsc = (
        (1, 'نزولی',),
        (2, 'صعودی',),
    )
    sort_by = forms.ChoiceField(
        label='مرتب سازی',
        widget=forms.Select(attrs={
            'class': 'form-control',
        }), choices=SORT_CHOICES, required=False)

    dsc_asc = forms.ChoiceField(
        label='اولویت',
        widget=forms.Select(attrs={
            'class': 'form-control',
        }), choices=sort_asc_dsc, required=False)
