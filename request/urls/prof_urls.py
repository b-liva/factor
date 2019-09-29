from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import request.views
# from z_mine.request.routers import router
from request.viewsFolder import proformaViews

urlpatterns = [
                  path('pro_form', proformaViews.pro_form, name='pro_form'),
                  path('pro_form_cookie/<int:req_id>', proformaViews.pro_form_cookie, name='pro_form_cookie'),
                  path('index', proformaViews.pref_index, name='pref_index'),
                  path('pref_index_cc', proformaViews.pref_index_cc, name='pref_index_cc'),
                  path('perm_clear_session', proformaViews.perm_clear_session, name='perm_clear_session'),
                  path('prefspec-index', proformaViews.prefspec_index, name='prefspec_index'),
                  path('prefspec-prefspec_clear_cache', proformaViews.prefspec_clear_cache,
                       name='prefspec_clear_cache'),
                  path('index-perms', proformaViews.perm_index, name='perm_index'),
                  path('user-perms', proformaViews.user_export, name='user_export'),
                  path('export-perms', proformaViews.perms_export, name='perm_export'),
                  path('request-perms', proformaViews.request_export, name='request_export'),
                  path('prof-export', proformaViews.prof_export, name='prof_export'),
                  path('perms-specs', proformaViews.perm_specs, name='perm_specs'),
                  path('index-deleted', proformaViews.pref_index_deleted, name='pref_index_deleted'),
                  path('find', proformaViews.pref_find, name='pref_find'),
                  path('<int:ypref_pk>/', include([
                      path('insert_form', proformaViews.pref_insert_spec_form, name='pref_insert_spec_form'),
                      path('', proformaViews.pref_details, name='pref_details'),
                      path('delete', proformaViews.pref_delete, name='pref_delete'),
                      path('prof-delete', proformaViews.delete_proforma_no_prefspec,
                           name='delete_proforma_no_prefspec'),
                      path('form', request.viewsFolder.proformaViews.pref_edit_form, name='pref_edit_form'),
                      path('edit', proformaViews.pref_edit, name='pref_edit'),
                      path('edit2', proformaViews.pref_edit2, name='pref_edit2'),
                      path('to-follow', proformaViews.to_follow, name='to_follow'),
                      path('prof_spec_form', request.viewsFolder.proformaViews.prof_spec_form, name='prof_spec_form'),
                      path('proforma-pdf/<render_header>/', request.viewsFolder.proformaViews.proforma_pdf, name='proforma_pdf'),
                  ])),
                  path('followup/<int:followup_pk>/', include([
                      path('delete', request.viewsFolder.proformaViews.followup_delete,
                           name='followup_delete'),
                  ])),
                  # path('api/', include(router.urls)),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
