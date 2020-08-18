import graphene
from graphene import relay, ObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id
from core.decorators import permission_required
from core.permissions import OrderPermissions
from core.utils import DeletePermissionCheck
from ..forms.forms import RequestModelForm, ReqSpecModelForm
from ..orders.types import RequestNode
from ...models import Requests, ReqSpec
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
        input['owner'] = str(owner.pk)
        attrs = ['req_id', 'rpm_new', 'im', 'ip', 'ic', 'type']
        input = graphql_utils.from_globad_bulk(attrs, input)

        kwargs = {"data": input}
        global_id = input.pop("id", None)
        if global_id:
            node_type, pk = from_global_id(global_id)
            instance = cls._meta.model._default_manager.get(pk=pk)
            kwargs["instance"] = instance

        return kwargs


class DeleteOrder(DeletePermissionCheck, relay.ClientIDMutation):

    class Input:
        id = graphene.ID()
        model = Requests
        label = 'درخواست'

    permission_list = [OrderPermissions.DELETE_REQUESTS]

    @classmethod
    @login_required
    @permission_required(permission_list)
    def mutate(cls, root, info, input):
        return super(DeleteOrder, cls).mutate(root, info, input)


class DeleteOrderSpec(DeletePermissionCheck, relay.ClientIDMutation):
    class Input:
        id = graphene.ID()
        model = ReqSpec
        label = 'ردیف'

    permission_list = [OrderPermissions.DELETE_REQSPEC]

    @classmethod
    @login_required
    @permission_required(permission_list)
    def mutate(cls, root, info, input):
        return super(DeleteOrderSpec, cls).mutate(root, info, input)


class RequestModelMutations(ObjectType):
    request_mutation = RequestModelFormMutation.Field()
    req_spec_mutation = ReqSpecModelFormMutation.Field()
    delete_order = DeleteOrder.Field()
    delete_order_spec = DeleteOrderSpec.Field()


