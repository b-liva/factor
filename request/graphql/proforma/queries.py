from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from .types import ProformaNode, PrefSpecNode


class Query(object):
    proforma = relay.Node.Field(ProformaNode)
    all_proformas = DjangoFilterConnectionField(ProformaNode)

    pref_spec = relay.Node.Field(PrefSpecNode)
    all_pref_specs = DjangoFilterConnectionField(PrefSpecNode)
