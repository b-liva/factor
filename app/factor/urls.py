"""factor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from graphene_django.views import GraphQLView
from graphql_jwt.decorators import jwt_cookie
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.viewsFolder.views import LoginAfterPasswordChangeView
import tender.views
import request.views
from factor import views as general_views


class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    pass


urlpatterns = [
                  path('admin/', admin.site.urls),
                  # path("graphql/", jwt_cookie(GraphQLView.as_view(graphiql=True))),
                  path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
                  # path("graphql/", GraphQLView.as_view(graphiql=True)),
                  path('accounts/password/change/', LoginAfterPasswordChangeView.as_view(),
                       name='account_change_password'),
                  path('accounts/', include('allauth.urls')),
                  # path('', prefactor.views.home, name='homepage'),
                  path('', request.views.dashboard, name='dashboard'),
                  path("vue", TemplateView.as_view(template_name="application.html"), name="app",),
                  path("vue2", TemplateView.as_view(template_name="index.html"), name="app",),
                  path('new-panel', request.views.new_panel, name='new_panel'),
                  path('dashboard2', request.views.dashboard2, name='dashboard2'),
                  path('sales_comparison', request.views.sales_comparison, name='sales_comparison'),
                  path('sales-dash', request.views.sales_expert_dashboard, name='dashboard'),
                  path('kwjs/', request.views.kwjs, name='kwjs'),
                  path('agentjs/', request.views.agentjs, name='agentjs'),
                  path('tenders/', tender.views.tenders, name='tenders'),
                  path('tenders_admin/', tender.views.tenders_admin, name='tenders_admin'),
                  path('dashboard/', request.views.dashboard, name="dashboard"),
                  path('errorpage/', request.views.errorpage, name="errorpage"),
                  path('account/', include('accounts.url')),
                  path('request/', include('request.urls.url')),
                  path('cost/', include('cost.urls'), name="cost"),
                  path('feature/', include('jfeature.urls')),
                  # path('api/request/', include('request.urls.url')),
                  path('customer/', include('customer.url')),
                  path('fund/', include('fund.url')),
                  path('pricedb/', include('pricedb.url')),
                  path('fund/', include('fund.url')),
                  path('speccm/', include('spec_communications.url')),
                  path('ereq/', include('req_track.url')),
                  path('motors/', include('motordb.url')),
                  # path('v1/request', include('request.urls.url')),
                  path('api/v1/fund/', include('fund.api.urls'), name='post-api'),
                  path('comming-soon', general_views.comming_soon, name='comming_soon'),
                  path('api/', include('api.url')),
                  path('api-auth/', include('rest_framework.urls'), name='rest_framework'),  # login route with rest_framework

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
# if settings.DEBUG:
#     import debug_toolbar
#
#     urlpatterns = [
#                       path('__debug__/', include(debug_toolbar.urls)),
#
#                       # For django versions before 2.0:
#                       # url(r'^__debug__/', include(debug_toolbar.urls)),
#
#                   ] + urlpatterns
