from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView
from api.v1 import mixins
from django.contrib.auth import get_user_model
User = get_user_model()
from customer.models import Customer


class Homeview(TemplateView):
    template_name = 'customers/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["games"] = 6
        return context


class HelloWorldVie(View):

    def get(self, request):
        return HttpResponse('HelloWorld!')


class CustomerListView(LoginRequiredMixin, mixins.PageTitleMixins, ListView):
    model = Customer
    """ there is no need to this line if current file and  the template are in the same folder """
    template_name = 'customers/customer_list.html'
    page_title = 'Customer List Page'

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return self.model.objects.filter(owner=self.request.user)
        return self.model.objects.all()


class CustomerDetailsView(LoginRequiredMixin, mixins.PageTitleMixins, DetailView, UpdateView):
    model = Customer
    fields = ('name', 'phone', 'email', 'owner',)
    template_name = 'customers/customer_details.html'
    context_object_name = 'customer_details'

    def get_page_title(self):
        obj = self.get_object()
        return "مشخصات " + obj.name


class CustomerCreateView(LoginRequiredMixin, mixins.PageTitleMixins, CreateView):
    model = Customer
    fields = ('name', 'phone', 'email', 'owner', 'code', 'code_temp', 'type', 'pub_date', 'date2', 'phone', 'fax', 'email', 'website')
    template_name = 'customers/customer_form.html'
    page_title = 'مشتری جدید'

    def get_initial(self):
        initial = super().get_initial()
        initial['name'] = 'change this name'
        initial['owner'] = User.objects.get(pk=3)
        return initial


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    fields = (
    'name', 'phone', 'email', 'owner', 'code', 'code_temp', 'type', 'pub_date', 'date2', 'phone', 'fax', 'email', 'website')
    template_name = 'customers/customer_form.html'

