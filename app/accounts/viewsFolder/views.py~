from allauth.account.views import PasswordChangeView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.urls import reverse_lazy

from accounts.forms import RegisterForm, LoginForm
from django.views.generic import CreateView, FormView


class CLoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/cbv/login.html'

    def form_valid(self, form):
        request = self.request
        username = form.cleaned_data.get("username")
        passwrod = form.cleaned_data.get("password")
        user = authenticate(request, usernam=username, passwrod=passwrod)
        if user is not None:
            login(request, user)
            return redirect('/dashboard')

        return super(CLoginView, self).form_invalid(form)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/cbv/register.html'
    success_url = '/dashboard/'


class LoginAfterPasswordChangeView(PasswordChangeView):

    # success_url = reverse_lazy("account_login")

    @property
    def success_url(self):
        return reverse_lazy('account_login')
