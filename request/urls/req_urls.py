from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import request.views
from request import views2
from request.filters.filters import RequestFilter
from .. import reqSpecViews
from django_filters.views import FilterView
from request.viewsFolder.request.request import (RequestList, RequestFilterView)

urlpatterns = [
    path('project_type', request.views2.project_type_form, name='project_type_form'),
    path('project-type/index', request.views2.projects_type_index, name='projects_type_index'),

    path('form', request.views2.request_form, name='request_form'),
    path('req_form', request.views2.req_form, name='req_form'),
    path('wrong_data', request.views2.wrong_data, name='wrong_data'),
    path('wrong_data2', request.views2.wrong_data2, name='wrong_data2'),
    path('req_form_copy', request.views2.req_form_copy, name='req_form_copy'),
    path('insert', request.views2.request_insert, name='request_insert'),
    path('index', request.views2.request_index, name='request_index'),
    path('index-p', request.views2.request_index_paginate, name='request_index_paginate'),
    path('index-vue', request.views2.request_index_vue, name='request_index_vue'),
    path('index-vue-deleted', request.views2.request_index_vue_deleted, name='request_index_vue_deleted'),
    path('requests', request.views2.req_search, name='req_search'),
    path('fsearch', request.views2.fsearch, name='fsearch'),
    path('fsearch3', request.views2.fsearch3, name='fsearch3'),
    path('fsearch2', request.views2.fsearch2, name='fsearch2'),
    path('search', RequestList.as_view(), name='req_search2'),
    # path('search-req', RequestSearch.as_view(), name='search_req'),
    path('fsearch5', request.views2.fsearch5, name='fsearch5'),
    path('search-req2', RequestFilterView.as_view(), name='search_req'),
    # path('<int:pk>/details', RequestDetailsView.as_view(), name='request_details_cbv'),
    path('<int:pk>/', include([
        # path('details', RequestDetailsView.as_view(), name='request_details_cbv'),
    ])),
    path('find', request.views2.request_find, name='request_find'),
    path('<int:request_pk>/', include([
        path('', request.views2.request_read, name='request_details'),
        path('read-vue', request.views2.read_vue, name='read_vue'),
        path('delete', request.views2.request_delete, name='request_delete'),
        path('edit', request.views2.request_edit, name='request_edit'),
        path('editForm', request.views2.request_edit_form, name='request_edit_form'),
        path('finish', request.views2.finish, name='request_finish'),
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
        path('copy', request.reqSpecViews.reqspec_copy, name='reqspec_copy'),
    ])),

]
