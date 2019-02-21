import jdatetime
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django_filters.views import FilterView
from request.filters.filters import RequestFilter, FilteredListView
from request.models import Requests
from request.forms.forms import RequestFrom, SpecForm
from request.forms.search import SpecSearchForm, ReqSearchForm


class RequestList(ListView):
    template_name = 'requests/admin_jemco/yrequest/search_index.html'
    model = Requests
    paginate_by = 20
    http_method_names = ['get', 'post']
    # queryset = Requests.objects.all()
    today = jdatetime.date.today()
    response = []
    filterset_class = RequestFilter

    # def get_queryset(self):
    #     return Requests.objects.filter(is_active=True).order_by('date_fa').reverse()

    def get_queryset(self):
        qs = Requests.objects.all()
        request_filtered_list = RequestFilter(self.request.GET, queryset=qs)
        return request_filtered_list.qs

    # def get_queryset(self):
    #     response = []
    #     requests = Requests.objects.filter(is_active=True).order_by('date_fa').reverse()
    #
    #     if not self.request.user.is_superuser:
    #         # requests = requests.filter(owner=self.request.user) | requests.filter(colleagues=self.request.user)
    #         # requests = requests.distinct()
    #         # this is also true
    #         requests = requests.filter(Q(owner=self.request.user) | Q(colleagues=self.request.user))
    #         requests = requests.distinct()
    #     """
    #             now filter the request by data of form
    #     """
    #
    #     try:
    #         name = self.kwargs['your_name']
    #     except:
    #         name = ''
    #     if name != '':
    #         requests = requests.filter(customer__name__icontains=name)
    #
    #     for req in requests:
    #         diff = self.today - req.date_fa
    #         # print(f'diff is: {diff.days}')
    #         response.append({
    #             'req': req,
    #             'delay': diff.days,
    #             'colleagues': req.colleagues.all(),
    #         })
    #     return response

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RequestList, self).get_context_data(**kwargs)
        # context['req_form'] = RequestFrom
        # context['spec_form'] = SpecForm
        # context['filter_items'] = SpecSearchForm
        context['req_search_form'] = ReqSearchForm
        # print(context)
        return context


# class RequestDetailsView(DetailView):
#     template_name = 'requests/admin_jemco/yrequest/cbv/details.html'
#     model = Requests
#     # slug_field = 'pk'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(RequestDetailsView, self).get_context_data(**kwargs)
#         print(context)
#         return context


class RequestFilterView(FilterView):
    filterset_class = RequestFilter,
    template_name = 'requests/admin_jemco/yrequest/search_index3.html'
    paginate_by = 20
    # context_object_name = 'req_list'
