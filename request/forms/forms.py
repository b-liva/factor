from django import forms
from django.db.models import Q
from django.utils.timezone import now
from request import models
from django.contrib.auth import get_user_model
User = get_user_model()

from request.models import Xpref, ProjectType, IMType, ICType, IEType, IPType, ReqPart


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
        fields = ('number', 'colleagues', 'date_fa', 'summary')
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
                'placeholder': 'لطفا شماره درخواست را بدون در نظر گرفتن سال وارد نمایید.',

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
        self.fields['type'].initial = ProjectType.objects.get(title='روتین')
        self.fields['im'].initial = IMType.objects.get(title='IMB3')
        self.fields['ip'].initial = IPType.objects.get(title='IP55')
        self.fields['ic'].initial = ICType.objects.get(title='IC411')
        self.fields['ie'].initial = IEType.objects.get(title='IE1')
        # list = [ 'images']
        list = ['sent', 'tech', 'price', 'permission', 'cancelled', 'finished']
        for visible in self.visible_fields():
            if visible.name not in list:
                visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.ReqSpec
        fields = '__all__'
        exclude = ('owner', 'req_id', 'is_active', 'ip_type', 'ic_type', 'price', 'permission', 'sent', 'rpm',)
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
            'finished': ('اختتام'),
        }


class SpecAddForm(SpecForm):
    
    class Meta(SpecForm.Meta):
        # exclude = SpecForm.Meta.exclude + ('sent', 'tech', 'price', 'permission')
        exclude = SpecForm.Meta.exclude


class PartForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PartForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ReqPart
        fields = ('qty', 'title', )
        labels = {
            'qty': 'تعداد',
            'title': 'شرح کالا',
        }


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
        super(ProformaForm, self).__init__(*args, **kwargs)
        self.fields['req_id'].queryset = models.Requests.objects.filter(is_active=True)\
            .filter(Q(owner=current_user) | Q(colleagues=current_user)).distinct()
        if User.objects.get(pk=current_user).is_superuser:
            self.fields['req_id'].queryset = models.Requests.objects.filter(is_active=True)

        # this renders the items in form drop down menu
        # self.fields['req_id'].label_from_instance = lambda obj: "%s" % obj.number

        list = ['verified']
        for visible in self.visible_fields():
            if visible.name not in list:
                visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.Xpref
        fields = ('req_id', 'number_td', 'date_fa', 'exp_date_fa', 'summary',)
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
            'number_td': 'شماره تدوین',
            'date_fa': 'تاریخ صدور',
            'exp_date_fa': 'تاریخ انقضا',
            'summary': 'جزئیات',
            'verified': 'تاییدیه',

        }


class ProformaEditForm(forms.ModelForm):

    def __init__(self, current_user, *args, **kwargs):
        print(f'current user is: {current_user}')
        super(ProformaEditForm, self).__init__(*args, **kwargs)

        list = ['verified', 'perm']
        for visible in self.visible_fields():
            if visible.name not in list:
                visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.Xpref
        fields = ('number_td', 'date_fa', 'exp_date_fa', 'perm_number', 'perm_date', 'due_date', 'summary', 'perm', 'issue_type')
        widgets = {

            'date_fa': forms.DateInput(attrs={
                'id': 'date_fa'
            }),
            'exp_date_fa': forms.DateInput(attrs={
                'id': 'exp_date_fa'
            }),
            'due_date': forms.DateInput(attrs={
                'id': 'due_date'
            }),
            'perm_date': forms.DateInput(attrs={
                'id': 'perm_date'
            })
        }

        labels = {
            'req_id': 'درخواست',
            'number': 'شماره پیشفاکتور',
            'number_td': 'شماره تدوین',
            'date_fa': 'تاریخ صدور',
            'exp_date_fa': 'تاریخ انقضا',
            'due_date': 'تاریخ تحویل',
            'summary': 'جزئیات',
            'verified': 'تاییدیه',
            'perm': 'مجوز',
            'perm_date': 'تاریخ مجوز',
            'perm_number': 'شماره مجوز',
            'issue_type': 'دلیل تأخیر',
        }


class ProfSpecForm(forms.ModelForm):

    class Meta:
        model = models.PrefSpec
        # fields = ('qty', 'price',)
        fields = '__all__'


class ProfPartForm(forms.ModelForm):

    class Meta:
        model = models.PrefPart
        fields = '__all__'


class RequestCopyForm(forms.Form):
    number = forms.IntegerField(label='شماره درخواست')
    new_number = forms.IntegerField(label='شماره جدید', required=False)


class ReqFollowUpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(ReqFollowUpForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.Requests
        fields = ('follow_up',)

        labels = {
            'follow_up': 'شرح پیگیری',
        }


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(CommentForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.Comment
        fields = ('body',)

        labels = {
            'body': 'شرح',
        }


class ProfFollowUpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(ProfFollowUpForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.ProformaFollowUP
        fields = '__all__'
        exclude = ('xpref', 'author', 'pub_date', 'description')
        widgets = {

            'date_fa': forms.DateInput(attrs={
                'id': 'date_fa'
            }),
            'next_followup': forms.DateInput(attrs={
                'id': 'exp_date_fa'
            })
        }
        labels = {
            'summary': 'شرح',
            'date_fa': 'تاریخ',
            'next_followup': 'تاریخ پیگیری بعدی',
        }