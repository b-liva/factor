from graphene import ObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from ..forms.forms import ProformaModelForm, PrefSpecForm


class ProformaModelMutation(DjangoModelFormMutation):
    class Meta:
        form_class = ProformaModelForm


class PrefSpecModelMutation(DjangoModelFormMutation):
    class Meta:
        form_class = PrefSpecForm


class ProformaModelMutation(ObjectType):
    proforma_mutation = ProformaModelMutation.Field()
    prefspec_mutation = PrefSpecModelMutation.Field()
