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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.viewsFolder.views import LoginAfterPasswordChangeView
import tender.views
import request.views
from factor import views as general_views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('accounts/password/change/', LoginAfterPasswordChangeView.as_view(),
                       name='account_change_password'),
                  path('accounts/', include('allauth.urls')),
                  # path('', prefactor.views.home, name='homepage'),
                  path('', request.views.dashboard, name='dashboard'),
                  path('dashboard2', request.views.dashboard2, name='dashboard'),
                  path('sales-dash', request.views.sales_expert_dashboard, name='dashboard'),
                  path('kwjs/', request.views.kwjs, name='kwjs'),
                  path('agentjs/', request.views.agentjs, name='agentjs'),
                  path('dashboard2', request.views.dashboard2, name='dashboard2'),
                  path('oldhomepage', request.views.allTable, name='allTables'),
                  path('tenders/', tender.views.tenders, name='tenders'),
                  path('tenders_admin/', tender.views.tenders_admin, name='tenders_admin'),
                  path('requests/', request.views.request_page, name="requestPage"),
                  path('requests/<int:request_id>', request.views.request_details, name="reqDetails"),
                  path('views/', request.views.prefactors_page, name="prefactorsPage"),
                  path('views/<int:pref_id>', request.views.prefactor_details, name="prefactorsDetailPage"),
                  path('prefVerification/', request.views.prefactors_verification_page, name="prefVerificationPage"),
                  path('prefVerification/<int:pref_ver_id>', request.views.pref_ver_details, name="prefVerfDetailPage"),
                  path('find_pref/', request.views.find_pref, name="find_prefPage"),
                  path('dashboard/', request.views.dashboard, name="dashboard"),
                  path('errorpage/', request.views.errorpage, name="errorpage"),
                  path('account/', include('accounts.url')),
                  path('request/', include('request.urls.url')),
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

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
