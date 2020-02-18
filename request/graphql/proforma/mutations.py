from graphene import ObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from ..forms.forms import ProformaModelForm, PrefSpecForm


class ProformaModelFormMutation(DjangoModelFormMutation):
    class Meta:
        form_class = ProformaModelForm


class PrefSpecModelFormMutation(DjangoModelFormMutation):
    class Meta:
        form_class = PrefSpecForm


class ProformaModelMutation(ObjectType):
    proforma_mutation = ProformaModelFormMutation.Field()
    prefspec_mutation = PrefSpecModelFormMutation.Field()
