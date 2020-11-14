import jdatetime
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


def count_per_project_type(project_type, days=None, **filters):

    specs = reqspecs_raw().filter(type__title=project_type)
    if days:
        specs = specs.filter(**filters)
    count = specs.values('req_id').distinct().count()

    return count


class Statistics(ObjectType):
    class Input:
        days = Int()
    total = Field(KwCounts, days=Int())
    routine = Field(KwCounts, days=Int())
    project = Field(KwCounts, days=Int())
    services = Field(KwCounts, days=Int())
    ex = Field(KwCounts, days=Int())

    def resolve_total(self, info, days):
        orders_filters = {
            'is_active': True
        }
        filters = {
            'req_id__is_active': True
        }

        if days:
            today = jdatetime.date.today()
            start_date = today - jdatetime.timedelta(days)
            orders_filters.update({
                'date_fa__gte': start_date
            })
            filters.update({
                'req_id__date_fa__gte': start_date
            })

        orders_active = Requests.objects.filter(**orders_filters)
        count = orders_active.count()

        rspec = ReqSpec.objects.filter(**filters)
        kw = calculate_kw(rspec)
        kw = 0 if not kw else kw
        count = 0 if not count else count

        return KwCounts(title='تعداد درخواست ها', kw=kw, count=count)

    def resolve_routine(self, info, days=None):
        filters = {
            'type__title': 'روتین'
        }
        if days:
            today = jdatetime.date.today()
            start_date = today - jdatetime.timedelta(days)
            filters.update({
                'req_id__date_fa__gte': start_date,
            })
        specs = reqspecs_raw().filter(**filters)
        kw = calculate_kw(specs)
        count = specs.values('req_id').distinct().count()

        kw = 0 if not kw else kw
        count = 0 if not count else count
        return KwCounts(title='روتین (KW)', kw=kw, count=count)

    def resolve_ex(self, info, days=None):
        filters = {
            'type__title': 'ضد انفجار'
        }
        if days:
            today = jdatetime.date.today()
            start_date = today - jdatetime.timedelta(days)
            filters.update({
                'req_id__date_fa__gte': start_date,
            })
        specs = reqspecs_raw().filter(**filters)
        kw = calculate_kw(specs)
        count = specs.values('req_id').distinct().count()

        kw = 0 if not kw else kw
        count = 0 if not count else count
        return KwCounts(title='ضدانفجار (KW)', kw=kw, count=count)

    def resolve_services(self, info, days=None):

        filters = {
            'type__title': 'تعمیرات'
        }
        if days:
            today = jdatetime.date.today()
            start_date = today - jdatetime.timedelta(days)
            filters.update({
                'req_id__date_fa__gte': start_date,
            })
        specs = reqspecs_raw().filter(**filters)
        kw = calculate_kw(specs)
        count = specs.values('req_id').distinct().count()

        kw = 0 if not kw else kw
        count = 0 if not count else count

        # kw = kw_per_project_type('تعمیرات')
        # count = count_per_project_type('تعمیرات')
        return KwCounts(title='تعمیرات (KW)', kw=kw, count=count)

    def resolve_project(self, info, days=None):
        filters = {
            'type__title': 'تعمیرات'
        }
        if days:
            today = jdatetime.date.today()
            start_date = today - jdatetime.timedelta(days)
            filters.update({
                'req_id__date_fa__gte': start_date,
            })
        specs = reqspecs_raw().filter(**filters)
        kw = calculate_kw(specs)
        count = specs.values('req_id').distinct().count()

        kw = 0 if not kw else kw
        count = 0 if not count else count

        # kw = kw_per_project_type('پروژه')
        # count = count_per_project_type('پروژه')
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

    dashboard_statistics = Field(Statistics, customer=ID(), days=Int())

    def resolve_dashboard_statistics(self, info, **kwargs):
        print(kwargs)
        return True
