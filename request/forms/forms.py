from django import forms
from django.utils.timezone import now
from request import models
from accounts.models import User


class ProjectTypeForm(forms.ModelForm):

    class Meta:
        model = models.ProjectType
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
            })
        }


class RequestFrom(forms.ModelForm):
    # number = forms.IntegerField()
    # pub_date = forms.DateTimeField(default=now)
    # image = forms.FileField()
    # summary = forms.Textarea(max_length=1000)

    def __init__(self, *args, **kwargs):
        super(RequestFrom, self).__init__(*args, **kwargs)
        self.fields['colleagues'].queryset = User.objects.filter(sales_exp=True)
        # this renders the items in form drop down menu
        # self.fields['req_id'].label_from_instance = lambda obj: "%s" % obj.number

    class Meta:
        model = models.Requests
        fields = '__all__'
        exclude = ('owner', 'pub_date', 'customer', 'added_by_customer', 'parent_number',
                   'edited_by_customer', 'is_active', 'temp_number', 'finished', 'date_finished')
        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-control',

            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Title here',

            }),
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شماره درخواست',

            }),
            'date_fa': forms.DateInput(attrs={
                'class': 'datetime-input form-control',
                'id': 'date_fa'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'شرح درخواست'
            }),
            'colleagues': forms.CheckboxSelectMultiple(attrs={
            })
        }

        labels = {
            'customer': ('مشتری'),
            'number': ('شماره درخواست'),
            'date_fa': ('تاریخ'),
            'colleagues': ('مشترک با'),
            'summary': ('جزئیات'),
        }


class RequestFileForm(forms.ModelForm):

    class Meta:
        model = models.RequestFiles
        fields = '__all__'
        exclude = ('req',)
        # widgets = {"image": forms.FileInput(attrs={'id': 'files', 'required': True, 'multiple': True})}
        widgets = {"image": forms.FileInput(attrs={'multiple': True})}
        labels = {
            'image': ('آپلود تصاویر'),
        }


class SpecForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SpecForm, self).__init__(*args, **kwargs)
        # list = [ 'images']
        list = ['sent', 'tech', 'price', 'permission', 'cancelled']
        for visible in self.visible_fields():
            if visible.name not in list:
                visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.ReqSpec
        fields = '__all__'
        exclude = ('owner', 'req_id', 'is_active')
        labels = {
            'qty': ('تعداد'),
            'type': ('نوع'),
            'kw': ('کیلووات'),
            'rpm': ('سرعت'),
            'voltage': ('ولتاژ'),
            'frame_size': ('فریم سایز'),
            'summary': ('جزئیات'),
            'sent': ('ارسال شده'),
            'tech': ('اطلاعات فنی'),
            'price': ('پیشنهاد مالی'),
            'permission': ('مجوز ساخت'),
            'cancelled': ('انصراف مشتری'),
        }


class SpecAddForm(SpecForm):
    
    class Meta(SpecForm.Meta):
        # exclude = SpecForm.Meta.exclude + ('sent', 'tech', 'price', 'permission')
        exclude = SpecForm.Meta.exclude


def user_choices(user):
    reqs = models.Requests.objects.filter(is_active=True).filter(owner=user)
    return reqs


class ProformaForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop('user')
    #
    #     super(ProformaForm, self).__init__(*args, **kwargs)
    #     self.fields['req_id'] = forms.ChoiceField(choices=user_choices(self.user))

    def __init__(self, current_user, *args, **kwargs):
        print(f'current user is: {current_user}')
        super(ProformaForm, self).__init__(*args, **kwargs)
        self.fields['req_id'].queryset = models.Requests.objects.filter(is_active=True).filter(owner=current_user)
        if User.objects.get(pk=current_user).is_superuser:
            self.fields['req_id'].queryset = models.Requests.objects.all()

        # this renders the items in form drop down menu
        # self.fields['req_id'].label_from_instance = lambda obj: "%s" % obj.number

        list = ['verified', ]
        for visible in self.visible_fields():
            if visible.name not in list:
                visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.Xpref
        fields = '__all__'
        exclude = ('owner', 'pub_date', 'is_active', 'temp_number')
        widgets = {

            'date_fa': forms.DateInput(attrs={
                'id': 'date_fa'
            }),
            'exp_date_fa': forms.DateInput(attrs={
                'id': 'exp_date_fa'
            })
        }

        labels = {
            'req_id': 'درخواست',
            'number': 'شماره پیشفاکتور',
            'date_fa': 'تاریخ صدور',
            'exp_date_fa': 'تاریخ انقضا',
            'summary': 'جزئیات',
            'verified': 'تاییدیه',

        }


class ProformaEditForm(forms.ModelForm):

    def __init__(self, current_user, *args, **kwargs):
        print(f'current user is: {current_user}')
        super(ProformaEditForm, self).__init__(*args, **kwargs)

        list = ['verified', ]
        for visible in self.visible_fields():
            if visible.name not in list:
                visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.Xpref
        fields = '__all__'
        exclude = ('owner', 'pub_date', 'is_active', 'req_id', 'temp_number')
        widgets = {

            'date_fa': forms.DateInput(attrs={
                'id': 'date_fa'
            }),
            'exp_date_fa': forms.DateInput(attrs={
                'id': 'exp_date_fa'
            })
        }

        labels = {
            'req_id': 'درخواست',
            'number': 'شماره پیشفاکتور',
            'date_fa': 'تاریخ صدور',
            'exp_date_fa': 'تاریخ انقضا',
            'summary': 'جزئیات',
            'verified': 'تاییدیه',

        }


class ProfSpecForm(forms.ModelForm):

    class Meta:
        model = models.PrefSpec
        # fields = ('qty', 'price',)
        fields = '__all__'


class RequestCopyForm(forms.Form):
    number = forms.IntegerField(label='شماره درخواست')
