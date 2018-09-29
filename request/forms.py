from django import forms
from django.utils.timezone import now


class RequestCreation(forms.Form):
    number = forms.IntegerField()
    pub_date = forms.DateTimeField(default=now)
    image = forms.FileField()

    summary = forms.Textarea(max_length=1000)