from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import request.views
from request.viewsFolder import proformaViews

urlpatterns = [
    path('pro_form', proformaViews.pro_form, name='pro_form'),
    path('pro_form_cookie/<int:req_id>', proformaViews.pro_form_cookie, name='pro_form_cookie'),
    path('index', proformaViews.pref_index, name='pref_index'),
    path('index-search', proformaViews.pref_search, name='pref_index'),
    path('index-perms', proformaViews.perm_index, name='perm_index'),
    path('user-perms', proformaViews.user_export, name='user_export'),
    path('export-perms', proformaViews.perms_export, name='perm_export'),
    path('request-perms', proformaViews.request_export, name='request_export'),
    path('perms-specs', proformaViews.perm_specs, name='perm_specs'),
    path('index-deleted', proformaViews.pref_index_deleted, name='pref_index_deleted'),
    path('find', proformaViews.pref_find, name='pref_find'),
    path('<int:ypref_pk>/', include([
      path('insert_form', proformaViews.pref_insert_spec_form, name='pref_insert_spec_form'),
      path('', proformaViews.pref_details, name='pref_details'),
      path('delete', proformaViews.pref_delete, name='pref_delete'),
      path('form', request.viewsFolder.proformaViews.pref_edit_form, name='pref_edit_form'),
      path('edit', proformaViews.pref_edit, name='pref_edit'),
      path('edit2', proformaViews.pref_edit2, name='pref_edit2'),
      path('prof_spec_form', request.viewsFolder.proformaViews.prof_spec_form, name='prof_spec_form'),
    ])),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
