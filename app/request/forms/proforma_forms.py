from django import forms
from django.utils.timezone import now
from request import models


class ProfFileForm(forms.ModelForm):

    class Meta:
        model = models.ProfFiles
        fields = '__all__'
        exclude = ('prof',)
        widgets = {"image": forms.FileInput(attrs={'multiple': True})}

        labels = {
            'image': ('آپلود تصاویر'),
        }


class ProfEditForm(forms.ModelForm):

    class Meta:
        model = models.Xpref
        fields = '__all__'
        exclude = ('req_id', 'owner', 'pub_date')
        widgets = {"image": forms.FileInput(attrs={'multiple': True})}


class ProfFollowUpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(ProfFollowUpForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.Xpref
        fields = ('follow_up',)

        labels = {
            'follow_up': 'شرح پیگیری',
        }


class DiscountForm(forms.Form):
    discount_value = forms.FloatField(label='درصد تخفیف')
