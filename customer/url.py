from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.customer, name='customer'),
    path('create', views.customer_create, name='customer_create'),
    path('view', views.customer_read, name='customer_view'),
    # path('update', views.customer_update, name='customer_update'),
    path('delete', views.customer_delete, name='customer_delete'),
    # path('customer_type/create', views.type_create, name='customer_type_create'),
    path('customer_type/view', views.type_read, name='customer_type_view'),
    # path('customer_type/update', views.type_update, name='customer_type_update'),
    path('customer_type/delete', views.type_delete, name='customer_type_delete'),
    path('testview', views.TestView.as_view(), name='testview'),


    path('form', views.customer_form, name='customer_form'),
    path('insert', views.customer_insert, name='customer_insert'),
    path('index', views.customer_index, name='customer_index'),
    path('<int:customer_pk>/', include([
        path('', views.customer_read2, name='customer_read'),
        path('edit', views.customer_edit, name='customer_edit'),
        path('delete', views.customer_delete, name='customer_delete'),

    ])),

    path('form', views.type_form, name='type_form'),
    path('insert', views.type_insert, name='type_insert'),
    path('index', views.type_index, name='type_index'),
    path('<int:type_pk>/', include([
        path('', views.type_read, name='type_read'),
        path('edit', views.type_edit, name='type_edit'),
        path('delete', views.type_delete, name='type_delete'),

    ])),
]