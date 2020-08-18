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
from pricedb import views
# import pricedb.views
# from pricedb import views
import pricedb
from pricedb.viewsFolder import views as generic

urlpatterns = [
  path('list', generic.IndexView.as_view(), name='price_set_list'),
  path('<int:pk>/', generic.DetailView.as_view(), name='price_set_details'),
  path('clean', pricedb.views.pricedb_clean, name='pricedb_clean'),
  path('form', pricedb.views.pricedb_form, name='pricedb_form'),
  path('insert', pricedb.views.pricedb_insert, name='pricedb_insert'),
  path('index', pricedb.views.pricedb_index, name='pricedb_index'),
  path('find', pricedb.views.pricedb_find, name='pricedb_find'),
  path('<int:pricedb_pk>/', include([
      path('', pricedb.views.pricedb_details, name='pricedb_details'),
      path('delete', pricedb.views.pricedb_delete, name='pricedb_delete'),
      path('edit', pricedb.views.pricedb_edit, name='pricedb_edit'),
  ])),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
