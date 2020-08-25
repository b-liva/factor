from django.db.models import Sum, F, FloatField
from graphene import relay, Field, List, String, Int, ID, GlobalID, ObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from customer.models import Customer
from .types import RequestNode, ReqSpecNode, ProjectTypeType, IMTypeNode, IPTypeNode, ICTypeNode, RpmTypeNode
from request.models import ProjectType, Requests, ReqSpec


class KwCounts(ObjectType):
    title = String()
    kw = Int()
    count = Int()

    # this override Statistics kw class
    # def resolve_kw(self, info):
    #     return 15987453


def active_orders():
    return Requests.objects.filter(is_active=True)


def reqspecs_raw():
    return ReqSpec.objects.filter(req_id__is_active=True)


def calculate_kw(rs):
    kw = rs.aggregate(
            kw=Sum(F('qty') * F('kw'), output_field=FloatField())
        )['kw']
    return kw


def kw_per_project_type(project_type):
    specs = reqspecs_raw().filter(type__title=project_type)
    kw = calculate_kw(specs)
    return kw


def count_per_project_type(project_type):
    specs = reqspecs_raw().filter(type__title=project_type)
    count = specs.values('req_id').distinct().count()
    return count


class Statistics(ObjectType):
    total = Field(KwCounts)
    routine = Field(KwCounts)
    project = Field(KwCounts)
    services = Field(KwCounts)
    ex = Field(KwCounts)

    def resolve_total(self, info):
        count = active_orders().count()
        rs = reqspecs_raw()
        kw = calculate_kw(rs)
        return KwCounts(title='تعداد درخواست ها', kw=kw, count=count)

    def resolve_routine(self, info):
        kw = kw_per_project_type('روتین')
        count = count_per_project_type('روتین')
        return KwCounts(title='روتین (KW)', kw=kw, count=count)

    def resolve_ex(self, info):
        kw = kw_per_project_type('ضد انفجار')
        count = count_per_project_type('ضد انفجار')
        return KwCounts(title='ضدانفجار (KW)', kw=kw, count=count)

    def resolve_services(self, info):
        kw = kw_per_project_type('تعمیرات')
        count = count_per_project_type('تعمیرات')
        return KwCounts(title='تعمیرات (KW)', kw=kw, count=count)

    def resolve_project(self, info):
        kw = kw_per_project_type('پروژه')
        count = count_per_project_type('پروژه')
        return KwCounts(title='پروژه (KW)', count=count, kw=kw)


class Query(ObjectType):

    request = relay.Node.Field(RequestNode)
    all_requests = DjangoFilterConnectionField(RequestNode)
    orders_no_proforma = DjangoFilterConnectionField(RequestNode)

    req_spec = relay.Node.Field(ReqSpecNode)
    all_req_Specs = DjangoFilterConnectionField(ReqSpecNode)

    project_type = Field(ProjectTypeType, id=Int(), title=String())
    all_project_types = DjangoFilterConnectionField(ProjectTypeType)

    def resolve_project_type(self, info, **kwargs):
        if 'id' in kwargs:
            id = kwargs.get('id')
            return ProjectType.objects.get(pk=id)
        if 'title' in kwargs:
            title = kwargs.get('title')
            return ProjectType.objects.get(title=title)
        return None

    def resolve_all_project_types(self, info, **kwargs):
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
