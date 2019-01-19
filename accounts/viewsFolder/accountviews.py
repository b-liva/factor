from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import (ListView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView
                                  )
from accounts.models import User
from customer.models import Customer
from accounts.formsDir.user_edit_forms import AccountUpdateForm, CustomerProfileUpdateForm
from braces import views as braces


class AccountListView(braces.PermissionRequiredMixin, ListView):
    template_name = 'accounts/cbv/list.html'
    model = User
    permission_required = 'accounts.index_user'
    redirect_unauthenticated_users = True
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AccountListView, self).get_context_data(object_list=None, **kwargs)
        # print(context)
        return context

    def no_permissions_fail(self, request=None):
        super(AccountListView, self).no_permissions_fail(request=None)
        messages.error(request, 'عدم دستری کافی!')
        return redirect('errorpage')


class AccountDetailsView(DetailView):
    template_name = 'accounts/cbv/details.html'
    model = User

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AccountDetailsView, self).get_context_data(object_list=None, **kwargs)
        print(context)
        return context


class AccountUpdateView(UpdateView):
    template_name = 'accounts/cbv/update.html'
    form_class = AccountUpdateForm
    model = User

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AccountUpdateView, self).get_context_data(object_list=None, **kwargs)
        print(context)
        return context


class CustomerProfileDetailsView(DetailView):
    template_name = 'accounts/cbv/customer_details.html'
    model = Customer

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CustomerProfileDetailsView, self).get_context_data(object_list=None, **kwargs)
        return context


class CustomerAccountUpdateView(AccountUpdateView):
    queryset = User.objects.filter(is_customer=True)
    # success_url = ''
    # def form_valid(self, form):
    #     super(CustomerAccountUpdateView, self).form_valid(form)
    #     form.save()


class CustomerProfileUpdateView(UpdateView):
    model = Customer
    # fields = '__all__'
    form_class = CustomerProfileUpdateForm
    template_name = 'accounts/cbv/customer_update.html'
