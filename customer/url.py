from django.urls import path, include
from . import views
from .viewsFolder.views import (
    CustomerRequestsListView,
    CustomerRequestDetailsView,
    CustomerCreateRequestview,
)

urlpatterns = [
    path('request/create', CustomerCreateRequestview.as_view(), name='customer_request_create'),

    path('request/<int:pk>/', include([
        path('', CustomerRequestDetailsView.as_view(), name='customer_request_details'),
    ])),
    path('<int:pk>/', include([
        path('dashboard', CustomerRequestsListView.as_view(), name='customer_dashboard'),
    ])),
    path('form', views.customer_form, name='customer_form'),
    path('cform', views.cform, name='cform'),
    path('insert', views.customer_insert, name='customer_insert'),
    path('repr/index', views.repr_index, name='repr_index'),
    path('index', views.customer_index, name='customer_index'),
    path('find', views.customer_find, name='customer_find'),
    path('<int:customer_pk>/', include([
        path('', views.customer_read2, name='customer_read'),
        path('dashboard', views.customer_read2, name='customer_dashboard'),
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

