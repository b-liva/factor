from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import tender.views
import request.views
from request import views2
from request import prefViews
from .. import reqSpecViews
from request.viewsFolder import permission, proformaViews

urlpatterns = [
    path('form', prefViews.pref_form, name='pref_form'),
    path('form2', prefViews.pref_form2, name='pref_form2'),
    path('pro_form', proformaViews.pro_form, name='pro_form'),
    path('insert', request.prefViews.pref_insert, name='pref_insert'),
    path('index', proformaViews.pref_index, name='pref_index'),
    path('index-deleted', proformaViews.pref_index_deleted, name='pref_index_deleted'),
    path('find', proformaViews.pref_find, name='pref_find'),
    path('<int:ypref_pk>/', include([
      path('insert_form', proformaViews.pref_insert_spec_form, name='pref_insert_spec_form'),
      path('', proformaViews.pref_details, name='pref_details'),
      # path('delete', request.prefViews.pref_delete, name='pref_delete'),
      path('delete', proformaViews.pref_delete, name='pref_delete'),
      path('form', request.prefViews.pref_edit_form, name='pref_edit_form'),
      path('edit', proformaViews.pref_edit, name='pref_edit'),
      path('edit2', proformaViews.pref_edit2, name='pref_edit2'),
      path('prof_spec_form', request.prefViews.prof_spec_form, name='prof_spec_form'),
    ])),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
