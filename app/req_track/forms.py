from django import forms

from django.contrib.auth import get_user_model
User = get_user_model()
from .models import ReqEntered, Payments


class E_Req_Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(E_Req_Form, self).__init__(*args, **kwargs)
        self.fields['owner'].queryset = User.objects.filter(sales_exp=True)

    class Meta:
        model = ReqEntered

        fields = "__all__"


class E_Req_Edit_Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(E_Req_Edit_Form, self).__init__(*args, **kwargs)
        ex_list = ['is_entered', 'red_flag']
        for visible in self.visible_fields():
            if visible.name not in ex_list:
                visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Payments

        fields = "__all__"
        exclude = ('is_entered', 'red_flag',)

        labels = {
            'number': 'شماره پرداخت',
            'prof_number': 'شماره پیش فاکتور',
            'date_txt': 'تاریخ',
            'amount': 'مبلغ',
            'type': 'نوع',
        }
