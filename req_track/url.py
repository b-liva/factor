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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views
urlpatterns = [
    path('add', views.e_req_add, name='e_req_add'),
    path('index', views.e_req_index, name='e_req_index'),
    path('<int:req_pk>/', include([
        path('', views.e_req_read, name='e_req_read'),
        path('del', views.e_req_delete, name='e_req_del'),
    ])),
    path('report', views.e_req_report, name='e_req_report'),
    path('report-proformas', views.e_req_report_proformas, name='e_req_report_prof'),
    path('report-payments', views.e_req_report_payments, name='e_req_report_payments'),
    path('check', views.check_orders, name='check_orders'),
    path('del_all', views.e_req_delete_all, name='ereq_del_all'),
]

