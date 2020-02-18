from graphene import ObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation

from ..forms.forms import PaymentModelForm


class PaymentModelFormMutation(DjangoModelFormMutation):
    class Meta:
        form_class = PaymentModelForm


class PaymentModelMutation(ObjectType):
    payment_mutation = PaymentModelFormMutation.Field()

