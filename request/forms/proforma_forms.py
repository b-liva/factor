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
