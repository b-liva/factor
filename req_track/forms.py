from django import forms

from accounts.models import User
from .models import ReqEntered


class E_Req_Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(E_Req_Form, self).__init__(*args, **kwargs)
        self.fields['owner'].queryset = User.objects.filter(sales_exp=True)

    class Meta:
        model = ReqEntered

        fields = "__all__"
