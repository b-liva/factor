from django import forms
from .models import SpecCommunications


class SpecCmForm(forms.ModelForm):

    class Meta:
        model = SpecCommunications
        fields = ('text', 'spec',)

