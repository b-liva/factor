from django.urls import path, include
from . import views
from .viewsFolder import fbv
from .viewsFolder.views import (
    CustomerRequestsListView,
    CustomerRequestDetailsView,
    CustomerCreateRequestview,
)
urlpatterns = [
    # FBV PATHS
    # path('request/create', fbv.custome_create_request2, name='fbv_customer_request_create'),
    path('dashboard', CustomerRequestsListView.as_view(), name='customer_dashboard'),
    path('request/create', fbv.custome_create_request, name='fbv_customer_request_create'),
    path('request/<int:req_pk>/', include([
        # path('details', fbv.customer_req_details, name='fbv_customer_request_details'),
        path('spec', fbv.customer_create_specs, name='fbv_customer_spec_create'),
        path('edit', fbv.customer_req_edit, name='fbv_customer_req_edit'),
    ])),

    path('<int:req_pk>/spec/<int:spec_pk>/', include([
        path('editForm', fbv.customer_spec_edit_form, name='fbv_customer_spec_edit_form'),
        path('delete', fbv.customer_spec_delete, name='fbv_customer_spec_delete'),
    ])),
    path('img_del/<int:img_pk>', fbv.customer_img_del, name='customer_img_del'),

    # CBV PATHS
    path('request/create', CustomerCreateRequestview.as_view(), name='customer_request_create'),

    path('request/<int:pk>/', include([
        path('', CustomerRequestDetailsView.as_view(), name='customer_request_details'),
    ])),
    path('<int:pk>/', include([
        # path('dashboard', CustomerRequestsListView.as_view(), name='customer_dashboard'),
    ])),
    path('form', views.customer_form, name='customer_form'),
    path('cform', views.cform, name='cform'),
    path('insert', views.customer_insert, name='customer_insert'),
    path('repr/index', views.repr_index, name='repr_index'),
    path('index', views.customer_index, name='customer_index'),
    path('find', views.customer_find, name='customer_find'),
    path('<int:customer_pk>/', include([
        path('', views.customer_read2, name='customer_read'),
        # path('dashboard', views.customer_read2, name='customer_dashboard'),
        path('edit', views.customer_edit, name='customer_edit'),
        path('editForm', views.customer_edit_form, name='customer_edit_form'),
        path('delete', views.customer_delete, name='customer_delete'),

    ])),

    path('<int:customer_pk>/addr/', include([
        path('add-address', views.add_address, name='add-address'),
        path('addr-list', views.addr_list, name='addr-list'),
        path('<int:addr_pk>/', include([
            path('add-phone', views.add_phone, name='add-phone'),
        ])),
    ])),

    path('type/form', views.type_form, name='type_form'),
    path('type/insert', views.type_insert, name='type_insert'),
    path('index', views.type_index, name='type_index'),
    path('<int:type_pk>/', include([
        path('', views.type_read, name='type_read'),
        path('edit', views.type_edit, name='type_edit'),
        path('delete', views.type_delete, name='type_delete'),

    ])),
    path('autocomplete', views.autocomplete, name='autocomplete'),
]


