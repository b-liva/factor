from graphene import relay, Field, List, String, Int
from graphene_django.filter import DjangoFilterConnectionField
from .types import RequestNode, ReqSpecNode, ProjectTypeType, IMTypeNode, IPTypeNode, ICTypeNode, RpmTypeNode
from request.models import ProjectType


class Query(object):
    request = relay.Node.Field(RequestNode)
    all_requests = DjangoFilterConnectionField(RequestNode)

    req_spec = relay.Node.Field(ReqSpecNode)
    all_req_Specs = DjangoFilterConnectionField(ReqSpecNode)

    project_type = Field(ProjectTypeType, id=Int(), title=String())
    all_project_types = List(ProjectTypeType)

    def resolve_project_type(self, info, **kwargs):
        print(info)
        if 'id' in kwargs:
            id = kwargs.get('id')
            return ProjectType.objects.get(pk=id)
        if 'title' in kwargs:
            title = kwargs.get('title')
            return ProjectType.objects.get(title=title)
        return None

    def resolve_all_project_types(self, info, **kwargs):
        print(info)
        return ProjectType.objects.all()

    rpm_type = relay.Node.Field(RpmTypeNode)
    all_rpm_types = DjangoFilterConnectionField(RpmTypeNode)

    im = relay.Node.Field(IMTypeNode)
    all_ims = DjangoFilterConnectionField(IMTypeNode)

    ip = relay.Node.Field(IPTypeNode)
    all_ips = DjangoFilterConnectionField(IPTypeNode)

    ic = relay.Node.Field(ICTypeNode)
    all_ics = DjangoFilterConnectionField(ICTypeNode)
