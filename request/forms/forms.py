from django import forms
from django.utils.timezone import now
from request import models


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

    class Meta:
        model = models.Requests
        fields = '__all__'
        exclude = ('owner', 'pub_date',)
        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-control',

            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Title here',

            }),
            'number': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Number here',

            }),
            'date_fa': forms.DateInput(attrs={
                'class': 'datetime-input form-control',
                'id': 'date_fa'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Summary Here...'
            })
        }


class RequestFileForm(forms.ModelForm):


    class Meta:
        model = models.RequestFiles
        fields = '__all__'
        exclude = ('req',)
        # widgets = {"image": forms.FileInput(attrs={'id': 'files', 'required': True, 'multiple': True})}
        widgets = {"image": forms.FileInput(attrs={'multiple': True})}


class SpecForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SpecForm, self).__init__(*args, **kwargs)
        # list = [ 'images']
        list = []
        for visible in self.visible_fields():
            if visible.name not in list:
                visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.ReqSpec
        fields = '__all__'
        exclude = ('owner', 'req_id')


def user_choices(user):
    reqs = models.Requests.objects.filter(owner=user)
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
        self.fields['req_id'].queryset = models.Requests.objects.filter(owner=current_user)
        # this renders the items in form drop down menu
        # self.fields['req_id'].label_from_instance = lambda obj: "%s" % obj.number

        list = []
        for visible in self.visible_fields():
            if visible.name not in list:
                visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.Xpref
        fields = '__all__'
        exclude = ('owner', 'pub_date', )
        widgets = {

            'date_fa': forms.DateInput(attrs={
                'id': 'date_fa'
            }),
            'exp_date_fa': forms.DateInput(attrs={
                'id': 'exp_date_fa'
            })
        }

        labels = {
            'req_id': 'Select The Request',
            'number': 'Enter Proforma Number',
            'date_fa': 'Date',
            'exp_date_fa': 'Expiry Date',
            'summary': 'Summary',

        }


class ProfSpecForm(forms.ModelForm):

    class Meta:
        model = models.PrefSpec
        # fields = ('qty', 'price',)
        fields = '__all__'
