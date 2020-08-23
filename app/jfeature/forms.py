from django import forms
from jfeature.models import Feature


class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ('title', 'description',)
        labels = {
            'title': 'عنوان',
            'description': 'توضیحات',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'توضیحات'
            })
        }
