from django.db.models import Sum, F, FloatField
from graphene import relay, Field, List, String, Int, ID, GlobalID, ObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from customer.models import Customer
from .types import RequestNode, ReqSpecNode, ProjectTypeType, IMTypeNode, IPTypeNode, ICTypeNode, RpmTypeNode
from request.models import ProjectType, Requests


class KwCounts(ObjectType):
    title = String()
    kw = Int()
    count = Int()

    def resolve_kw(self, info):
        return 15987453


class Statistics(ObjectType):
    total = Field(KwCounts)
    routine = Field(KwCounts)
    project = Field(KwCounts)
    services = Field(KwCounts)
    ex = Field(KwCounts)

    def resolve_total(self, info):
        count = Requests.objects.filter(is_active=True).count()
        reqs = Requests.objects.filter(is_active=True)
        kw = 0
        for req in reqs:
            kw += req.total_kw()
        return KwCounts(title='تعداد درخواست ها', kw=kw, count=count)

    def resolve_routine(self, info):
        count = 100
        kw = 2500
        return KwCounts(title='روتین (KW)', kw=kw, count=count)

    def resolve_ex(self, info):
        count = 10
        kw = 1354
        return KwCounts(title='ضدانفجار (KW)', kw=kw, count=count)

    def resolve_services(self, info):
        count = 456
        kw = 9874
        return KwCounts(title='تعمیرات (KW)', kw=kw, count=count)

    def resolve_project(self, info):
        return KwCounts(title='پروژه (KW)', count=125)


class Query(ObjectType):

    request = relay.Node.Field(RequestNode)
    all_requests = DjangoFilterConnectionField(RequestNode)
    orders_no_proforma = DjangoFilterConnectionField(RequestNode)

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

    dashboard_statistics = Field(Statistics, customer=ID())

    def resolve_dashboard_statistics(self, info, **kwargs):
        return True
