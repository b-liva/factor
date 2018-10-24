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

# from fund import views
# from motordb import views
import fund.views
import motordb.views

urlpatterns = [
  path('form', motordb.views.motordb_form, name='motordb_form'),
  path('view', motordb.views.test_view, name='test_view'),
  path('view2', motordb.views.test_view2, name='test_view2'),
  path('delall', motordb.views.del_all_motors, name='del_all_motors'),
  path('insert', motordb.views.motordb_insert, name='motordb_insert'),
  path('index', motordb.views.motordb_index, name='motordb_index'),
  path('find', motordb.views.motordb_find, name='motordb_find'),
  path('search_form', motordb.views.motordb_search_form, name='motordb_search_form'),
  path('search', motordb.views.motordb_search, name='motordb_search'),
  path('<int:motordb_pk>/', include([
      path('', motordb.views.motordb_details, name='motordb_details'),
      path('delete', motordb.views.motordb_delete, name='motordb_delete'),
      path('edit_form', motordb.views.motordb_edit_form, name='motordb_edit_form'),
      path('edit', motordb.views.motordb_edit, name='motordb_edit'),
  ])),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)