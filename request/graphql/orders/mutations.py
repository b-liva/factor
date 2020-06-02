import graphene
from graphene import relay, ObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_relay import from_global_id

from accounts.models import User
from ..forms.forms import RequestModelForm, ReqSpecModelForm
from ..orders.types import RequestNode
from ...models import Requests
from utils.graphql import utils as graphql_utils


class RequestModelFormMutation(DjangoModelFormMutation):

    order = relay.node.Field(RequestNode)

    class Meta:
        form_class = RequestModelForm

    @classmethod
    def get_form_kwargs(cls, root, info, **input):
        owner = info.context.user
        input['owner'] = str(owner.pk)
        attrs = ['customer']
        input = graphql_utils.from_globad_bulk(attrs, input)
        print(input)
        if 'colleagues' in input:
            input['colleagues'] = [from_global_id(colleague_pk)[1] for colleague_pk in input['colleagues']]

        kwargs = {"data": input}
        global_id = input.pop("id", None)
        if global_id:
            node_type, pk = from_global_id(global_id)
            instance = cls._meta.model._default_manager.get(pk=pk)
            kwargs["instance"] = instance

        return kwargs


class ReqSpecModelFormMutation(DjangoModelFormMutation):
    class Meta:
        form_class = ReqSpecModelForm

    @classmethod
    def get_form_kwargs(cls, root, info, **input):
        owner = info.context.user
        owner = User.objects.get(pk=4)
        input['owner'] = str(owner.pk)
        attrs = ['req_id', 'rpm_new', 'im', 'ip', 'ic']
        input = graphql_utils.from_globad_bulk(attrs, input)

        kwargs = {"data": input}
        global_id = input.pop("id", None)
        if global_id:
            node_type, pk = from_global_id(global_id)
            instance = cls._meta.model._default_manager.get(pk=pk)
            kwargs["instance"] = instance

        return kwargs


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


