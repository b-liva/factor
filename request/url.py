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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

