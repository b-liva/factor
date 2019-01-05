import jdatetime
from django.db.models import Q
from django.views.generic import ListView, DetailView
from request.models import Requests
from request.forms.forms import RequestFrom, SpecForm


class RequestList(ListView):
    template_name = 'requests/admin_jemco/yrequest/search_index.html'
    model = Requests
    paginate_by = 20
    http_method_names = ['post', 'get']
    # queryset = Requests.objects.all()
    today = jdatetime.date.today()
    response = []

    def get_queryset(self):
        response = []
        # request = self.request
        requests = Requests.objects.all().order_by('date_fa').reverse()

        if not self.request.user.is_superuser:
            # requests = requests.filter(owner=self.request.user) | requests.filter(colleagues=self.request.user)
            # this is also true
            requests = requests.filter(Q(owner=self.request.user) | Q(colleagues=self.request.user))
        for req in requests:
            diff = self.today - req.date_fa
            print(f'diff is: {diff.days}')
            response.append({
                'req': req,
                'delay': diff.days,
                'colleagues': req.colleagues.all(),
            })
        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RequestList, self).get_context_data(**kwargs)
        context['req_form'] = RequestFrom
        context['spec_form'] = SpecForm
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
