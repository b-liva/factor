from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import request.views
from request import views2
from .. import reqSpecViews

urlpatterns = [
    path('project_type', request.views2.project_type_form, name='project_type_form'),
    path('project-type/index', request.views2.projects_type_index, name='projects_type_index'),

    path('form', request.views2.request_form, name='request_form'),
    path('req_form', request.views2.req_form, name='req_form'),
    path('insert', request.views2.request_insert, name='request_insert'),
    path('index', request.views2.request_index, name='request_index'),
    path('find', request.views2.request_find, name='request_find'),
    path('<int:request_pk>/', include([
        path('', request.views2.request_read, name='request_details'),
        path('delete', request.views2.request_delete, name='request_delete'),
        path('edit', request.views2.request_edit, name='request_edit'),
        path('editForm', request.views2.request_edit_form, name='request_edit_form'),
      ])),

    path('<int:req_pk>/reqSpec/form', reqSpecViews.reqspec_form, name='reqSpec_form'),
    path('<int:req_pk>/reqSpec/spec_form', reqSpecViews.spec_form, name='spec_form'),
    path('reqSpec/insert', request.reqSpecViews.reqspec_insert, name='reqSpec_insert'),
    path('reqSpec/index', request.reqSpecViews.reqspec_index, name='reqSpec_index'),
    path('<int:req_pk>/reqSpec/<int:yreqSpec_pk>/', include([
        path('', request.reqSpecViews.reqspec_details, name='reqSpec_details'),
        path('delete', request.reqSpecViews.reqspec_delete, name='reqSpec_delete'),
        path('edit', request.reqSpecViews.reqspec_edit, name='reqSpec_edit'),
        path('editForm', request.reqSpecViews.reqspec_edit_form, name='reqspec_edit_form'),
    ])),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
