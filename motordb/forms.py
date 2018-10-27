from django import forms
from django.core import validators
from motordb import models

# def check_for_z(value):
#     if value[0] != 'z':
#         raise forms.ValidationError('needs to start with z')


class Motors(forms.Form):
    # name = forms.CharField(validators=[check_for_z])
    name = forms.CharField()
    kw = forms.IntegerField()
    speed = forms.IntegerField()
    # image = forms.ImageField(widget=forms.ImageField)
    # date = forms.DateField(widget=forms.DateField)
    botcatcher = forms.CharField(required=False,
                                 widget=forms.HiddenInput,
                                 validators=[validators.MaxLengthValidator(0)]
                                 )

    # def clean_botcatcher(self):
    #     botcather = self.cleaned_data['botcatcher']
    #     if len(botcather) > 0:
    #         raise forms.ValidationError('Gotcha Bot!')


class FormTest(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    verify_email = forms.EmailField(label='Enter Your Email Again')
    text = forms.CharField(widget=forms.Textarea)

    def clean(self):
        all_clean_data = super().clean()
        email = all_clean_data['email']
        vemail = all_clean_data['verify_email']

        if email != vemail:
            raise forms.ValidationError('make sure emails match')


class MotorsForm(forms.ModelForm):
    class Meta:
        model = models.Motors
        fields = '__all__'


class SearchForm(forms.ModelForm):
    class Meta:
        models = models.Motors
        fields = ['kw', 'speed', 'voltage']
