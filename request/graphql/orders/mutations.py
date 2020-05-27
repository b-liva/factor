import graphene
from graphene import relay, ObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_relay import from_global_id

from ..forms.forms import RequestModelForm, ReqSpecModelForm
from ..orders.types import RequestNode
from ...models import Requests


class RequestModelFormMutation(DjangoModelFormMutation):
    order = relay.node.Field(RequestNode)

    class Meta:
        form_class = RequestModelForm


class ReqSpecModelFormMutation(DjangoModelFormMutation):
    class Meta:
        form_class = ReqSpecModelForm


class DeleteOrder(relay.ClientIDMutation):
    class Input:
        order_id = graphene.ID()

    msg = graphene.String()
    number = graphene.Int()

    @classmethod
    def mutate_and_get_payload(cls, root, info, order_id):
        pid = from_global_id(order_id)[1]
        order = Requests.objects.get(pk=pid)
        order.delete()
        return cls(
            msg=f"درخواست خرید شماره {order.number} با موفقیت حذف گردید.",
            number=order.number
        )


class RequestModelMutations(ObjectType):
    request_mutation = RequestModelFormMutation.Field()
    req_spec_mutation = ReqSpecModelFormMutation.Field()
    delete_order = DeleteOrder.Field()


