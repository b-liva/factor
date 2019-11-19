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
app_name = 'req_track'
urlpatterns = [
    path('add', views.e_req_add, name='e_req_add'),
    path('index', views.e_req_index, name='e_req_index'),
    path('<int:req_pk>/', include([
        path('', views.e_req_read, name='e_req_read'),
        path('edit', views.e_req_edit, name='e_req_edit'),
        path('del', views.e_req_delete, name='e_req_del'),
    ])),
    path('check', views.check_orders, name='check_orders'),
    path('del_all', views.e_req_delete_all, name='ereq_del_all'),
    path('payments-list', views.payment_index, name='payment_index'),
    path('payments-check', views.payment_check, name='payment_check'),
    path('assign-payments', views.payment_assign, name='payment_assign'),
    path('motor_codes_index', views.motor_codes_index, name='motor_codes_index'),
    path('motor_codes_check', views.motor_codes_check, name='motor_codes_check'),
    path('motor_codes_process', views.motor_codes_process, name='motor_codes_process'),
    path('proformas', views.proformas, name='proformas'),
    path('proformas_complete', views.proformas_complete, name='proformas_complete'),
    path('proformas_uncomplete', views.proformas_uncomplete, name='proformas_uncomplete'),
    path('check_proforma', views.check_proforma, name='check_proforma'),
    path('create_proforma', views.create_proforma, name='create_proforma'),
    path('clear-flags', views.clear_flags, name='clear_flags'),
    path('prof_followup_list', views.prof_followup_list, name='prof_followup_list'),
    path('prof_followup_list2', views.prof_followup_list2, name='prof_followup_list2'),
    path('prof_followup_find', views.prof_followup_find, name='prof_followup_find'),
    path('prof_followup_form/<int:prof_pk>', views.prof_followup_form, name='prof_followup_form'),
    path('req_followup_form/<int:req_pk>', views.req_followup_form, name='req_followup_form'),
    path('customer-compare', views.customer_compare, name='customer_compare'),
    path('customer-compare-list', views.customer_compare_list, name='customer_compare_list'),
    path('customer-compare', views.customer_compare, name='customer_compare'),
    path('customer-compare-entered', views.customer_compare_entered, name='customer_compare_entered'),
    path('customer-status-update', views.customer_status_update, name='customer_compare_update'),
    path('customer-entered', views.customer_entered, name='customer_entered'),
    path('perms-index', views.perms_index, name='perms_index'),
    path('modify-perms', views.modify_perm, name='modify_perm'),
    path('perms-not-entered', views.perms_not_entered, name='perms_not_entered'),
    path('update_data_from_tadvin', views.update_data_from_tadvin, name='update_data_from_tadvin'),
    path('data', views.data, name='data'),
    path('data_process_first', views.data_process_first, name='data_process_first')

]

