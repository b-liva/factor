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

from fund import views
import fund.views

urlpatterns = [
  path('form', fund.views.fund_form, name='fund_form'),
  path('insert', fund.views.fund_insert, name='fund_insert'),
  path('index', fund.views.fund_index, name='fund_index'),
  path('find', fund.views.fund_find, name='fund_find'),
  path('<int:fund_pk>/', include([
      path('', fund.views.fund_details, name='fund_details'),
      path('delete', fund.views.fund_delete, name='fund_delete'),
      path('edit', fund.views.fund_edit, name='fund_edit'),
  ])),


  path('<int:fund_pk>/expense/form', fund.views.expense_form, name='expense_form'),
  path('expense/insert', fund.views.expense_insert, name='expense_insert'),
  path('expense/index', fund.views.expense_index, name='expense_index'),
  path('<int:fund_pk>/expense/find', fund.views.expense_find, name='expense_find'),
  path('<int:fund_pk>/expense/<int:expense_pk>/', include([
      path('', fund.views.expense_details, name='expense_details'),
      path('delete', fund.views.expense_delete, name='expense_delete'),
      path('edit', fund.views.expense_edit, name='expense_edit'),
  ])),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)