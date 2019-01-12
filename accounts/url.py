from django.urls import path, include
from . import views
from django.contrib.auth.views import (
    password_reset,
    password_reset_complete,
    password_reset_confirm,
    password_reset_done,
)
from accounts.viewsFolder.views import RegisterView, CLoginView
from accounts.viewsFolder.accountviews import (
    AccountListView,
    AccountDetailsView,
    AccountUpdateView,
    CustomerAccountUpdateView,
    CustomerProfileUpdateView,
    CustomerProfileDetailsView,
)


urlpatterns = [
    path('list', AccountListView.as_view(), name='account-list'),
    path('<int:pk>/', include([
        path('', AccountDetailsView.as_view(), name='account-details'),
        path('update', AccountUpdateView.as_view(), name='account_update'),
        path('customer-update', CustomerAccountUpdateView.as_view(), name='customer_account_update'),
        path('customer-profile', CustomerProfileDetailsView.as_view(), name='customer_profile'),
        path('customer-profile-update', CustomerProfileUpdateView.as_view(), name='customer_profile_update'),
    ])),
    path('register', RegisterView.as_view(), name='register'),
    path('clogin', CLoginView.as_view(), name='clogin'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('profile/edit', views.edit_profile, name='edit-profile'),
    path('profile/change-password', views.change_password, name='change-password'),
    path('reset-password', password_reset, name='reset_password'),
    path('reset-password/done', password_reset_done, name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    path('reset-password/complete/', password_reset_complete, name='password_reset_complete'),
    # path('', include('django.contrib.auth.urls')),
]
