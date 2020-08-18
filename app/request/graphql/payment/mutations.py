import graphene
from graphene import ObjectType, relay
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_jwt.decorators import login_required

from core.decorators import permission_required
from core.utils import DeletePermissionCheck
from core.permissions import PaymentPermissions
from ..forms.forms import PaymentModelForm
from ...models import Payment


class PaymentModelFormMutation(DjangoModelFormMutation):
    class Meta:
        form_class = PaymentModelForm


class DeletePayment(DeletePermissionCheck, relay.ClientIDMutation):
    class Input:
        id = graphene.ID()
        model = Payment
        label = 'دریافتی'

    permission_list = [PaymentPermissions.DELETE_PAYMENT]

    @classmethod
    @login_required
    @permission_required(permission_list)
    def mutate(cls, root, info, input):
        return super(DeletePayment, cls).mutate(root, info, input)


class PaymentModelMutation(ObjectType):
    payment_mutation = PaymentModelFormMutation.Field()
    delete_payment = DeletePayment.Field()

