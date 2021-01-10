from django.urls import path, include
from django.views.generic import TemplateView

import request.views
from request import views2
from .. import reqSpecViews


urlpatterns = [
    path('req_form', request.views2.req_form, name='req_form'),
    path('wrong_data', request.views2.wrong_data, name='wrong_data'),
    path('req_form_copy', request.views2.req_form_copy, name='req_form_copy'),
    path('index-exp', request.views2.index_by_month_exp, name='index_by_month_exp'),
    path('spec_export', request.views2.spec_export, name='spec_export'),
    path('index-vue-deleted', request.views2.request_index_vue_deleted, name='request_index_vue_deleted'),
    path('spec-search', request.views2.reqspec_search, name='reqspec_search'),
    path('reqspec_clear_cache', request.views2.reqspec_clear_cache, name='reqspec_clear_cache'),
    path('fsearch3', request.views2.fsearch3, name='fsearch3'),
    path('request-report', request.views2.req_report, name='req_report'),
    path('request_report_cc', request.views2.request_report_cc, name='request_report_cc'),
    path('find', request.views2.request_find, name='request_find'),
    path('reqSpec/index', request.reqSpecViews.reqspec_index, name='reqSpec_index'),
    path('index-no-summary', request.reqSpecViews.reqspec_index_no_summary, name='reqspec_index_no_summary'),
    path("vue", TemplateView.as_view(template_name="requests/admin_jemco/yrequest/vue/index_test.html"), name="req_app", ),

    path('reqspec_index_no_summary_no_routine', request.reqSpecViews.reqspec_index_no_summary_no_routine,
         name='reqspec_index_no_summary_no_routine'),
    path('reqspec_index_with_summary', request.reqSpecViews.reqspec_index_with_summary,
         name='reqspec_index_with_summary'),
    path('reqspec_index_IE', request.reqSpecViews.reqspec_index_IE, name='reqspec_index_IE'),
    path('assign-code-motor', request.reqSpecViews.assign_code_to_motor, name='assign_code_to_motor'),
    path('<int:request_pk>/', include([
        path('', request.views2.request_read, name='request_details'),
        path('delete', request.views2.request_delete, name='request_delete'),
        path('editForm', request.views2.request_edit_form, name='request_edit_form'),
        path('finish', request.views2.finish, name='request_finish'),
        path('order_valid', request.views2.order_valid, name='order_valid'),
        path('req-to-follow', request.views2.req_to_follow, name='req_to_follow'),
        path('reqSpec/form', reqSpecViews.reqspec_form, name='reqSpec_form'),
        path('spec_form', reqSpecViews.spec_form, name='spec_form'),
        path('part_form', reqSpecViews.part_form, name='part_form'),
        path('reqSpec/<int:yreqSpec_pk>/', include([
            path('delete', request.reqSpecViews.reqspec_delete, name='reqSpec_delete'),
            path('edit', request.reqSpecViews.reqspec_edit, name='reqSpec_edit'),
            path('editForm', request.reqSpecViews.reqspec_edit_form, name='reqspec_edit_form'),
            path('copy', request.reqSpecViews.reqspec_copy, name='reqspec_copy'),
        ])),
    ])),
]
