from graphene import relay, ObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from ..forms.forms import RequestModelForm, ReqSpecModelForm
from ..orders.types import RequestNode


class RequestModelFormMutation(DjangoModelFormMutation):
    order = relay.node.Field(RequestNode)

    class Meta:
        form_class = RequestModelForm


class ReqSpecModelFormMutation(DjangoModelFormMutation):
    class Meta:
        form_class = ReqSpecModelForm


class RequestModelMutations(ObjectType):
    request_mutation = RequestModelFormMutation.Field()
    req_spec_mutation = ReqSpecModelFormMutation.Field()


