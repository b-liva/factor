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

import prefactor.views
import prefactor_verification.views
import tender.views
import request.views
from request import views2
from request import prefViews
from . import reqSpecViews
from .viewsFolder import permission


urlpatterns = [
    path('request/', request.views.createpage, name='createpage'),
    path('request/create/', request.views.create_req, name='create_req'),
    path('createprefpage/', request.views.createprefpage, name='createprefpage'),
    path('create_pref/', request.views.create_pref, name='create_pref'),
    path('create_verf_page/', request.views.create_verf_page, name='create_verf_page'),
    path('create_verf/', request.views.create_verf, name='create_verf'),

    path('<req_pk>/spec/create', request.views.create_spec, name='create_spec'),
    path('spec/save', request.views.save_spec, name='save_spec'),
    path('<req_pk>/spec/<spec_pk>/update', request.views.edit_xspec, name='edit_xspec'),
    path('del_spec/<int:spec_id>', request.views.del_spec, name='del_spec'),

    path('find_pref', request.views.allTable, name='find_pref'),
    path('create_pref_spec', request.views.create_pref_spec, name='create_pref_spec'),
    path('create_spec_pref_findReq', request.views.create_spec_pref_findReq, name='create_spec_pref_findReq'),
    path('save_pref_spec', request.views.save_pref_spec, name='save_pref_spec'),
    path('xreq_pref_spec', request.views.xreq_pref_spec, name='xreq_pref_spec'),
    path('find_xpref', request.views.find_xpref, name='find_xpref'),
    path('xpref_link/<int:xpref_id>', request.views.xpref_link, name='xpref_link'),
    path('edit_xpref/<int:xpref_id>', request.views.edit_xpref, name='edit_xpref'),
    path('add_payment_page', request.views.add_payment_page, name='add_payment_page'),
    path('add_payment', request.views.add_payment, name='add_payment'),
    path('payments', request.views.payments, name='payments'),
    path('xpref_ver_create', request.views.xpref_ver_create, name='xpref_ver_create'),
    path('create_xverf', request.views.create_xverf, name='create_xverf'),



    path('form', request.views2.request_form, name='request_form'),
    path('insert', request.views2.request_insert, name='request_insert'),
    path('index', request.views2.request_index, name='request_index'),
    path('find', request.views2.request_find, name='request_find'),
    path('<int:request_pk>/', include([
        path('', request.views2.request_read, name='request_details'),
        path('delete', request.views2.request_delete, name='request_delete'),
        path('edit', request.views2.request_edit, name='request_edit'),
      ])),

    path('pref_spec/add', request.views2.pref_spec_add, name='pref_spec_add'),
    path('pref_spec/<int:ypref_spec_pk>/', include([
        path('', request.views2.pref_spec_details, name='prefspec_details'),
        path('delete', request.views2.pref_spec_del, name='pref_spec_delete'),
        path('edit', request.views2.pref_spec_edit, name='pref_spec_edit'),
    ])),

    path('permission/form', permission.permission_form, name='permission_form'),
    path('permission/insert', permission.permission_insert, name='permission_insert'),
    path('permission/index', permission.permission_index, name='permission_index'),
    path('permission/find', permission.permission_find, name='permission_find'),
    path('permission/<int:permission_pk>/', include([
        path('', permission.permission_details, name='permission_details'),
        path('delete', permission.permission_delete, name='permission_delete'),
        path('edit', permission.permission_edit, name='permission_edit'),
    ])),

    path('payment/form', request.views2.payment_form, name='payment_form'),
    path('payment/insert', request.views2.payment_insert, name='payment_insert'),
    path('payment/index', request.views2.payment_index, name='payment_index'),
    path('payment/find', request.views2.payment_find, name='payment_find'),
    path('payment/<int:ypayment_pk>/', include([
        path('', request.views2.payment_details, name='payment_details'),
        path('delete', request.views2.payment_delete, name='payment_delete'),
        path('edit', request.views2.payment_edit, name='payment_edit'),
    ])),

    path('pref/form', prefViews.pref_form, name='pref_form'),
    path('pref/form2', prefViews.pref_form2, name='pref_form2'),
    path('pref/insert', request.prefViews.pref_insert, name='pref_insert'),
    path('pref/index', request.prefViews.pref_index, name='pref_index'),
    path('pref/find', request.prefViews.pref_find, name='pref_find'),
    path('pref/<int:ypref_pk>/', include([
        path('', request.prefViews.pref_details, name='pref_details'),
        path('delete', request.prefViews.pref_delete, name='pref_delete'),
        path('form', request.prefViews.pref_edit_form, name='pref_edit_form'),
        path('edit', request.prefViews.pref_edit, name='pref_edit'),
    ])),

    path('<int:req_pk>/reqSpec/form', reqSpecViews.reqspec_form, name='reqSpec_form'),
    path('reqSpec/insert', request.reqSpecViews.reqspec_insert, name='reqSpec_insert'),
    path('reqSpec/index', request.reqSpecViews.reqspec_index, name='reqSpec_index'),
    path('<int:req_pk>/reqSpec/<int:yreqSpec_pk>/', include([
        path('', request.reqSpecViews.reqspec_details, name='reqSpec_details'),
        path('delete', request.reqSpecViews.reqspec_delete, name='reqSpec_delete'),
        path('edit', request.reqSpecViews.reqspec_edit, name='reqSpec_edit'),
    ])),

    # path('pref/form', views2.pref_add, name='ypref_add'),
    # path('pref/insert', views2.pref_insert, name='ypref_insert'),
    # path('pref/<int:ypref_pk>/', views2.pref, name='ypref'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
