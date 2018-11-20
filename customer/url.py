from django.urls import path, include
from . import views

urlpatterns = [

    path('form', views.customer_form, name='customer_form'),
    path('cform', views.cform, name='cform'),
    path('insert', views.customer_insert, name='customer_insert'),
    path('index', views.customer_index, name='customer_index'),
    path('find', views.customer_find, name='customer_find'),
    path('<int:customer_pk>/', include([
        path('', views.customer_read2, name='customer_read'),
        path('edit', views.customer_edit, name='customer_edit'),
        path('editForm', views.customer_edit_form, name='customer_edit_form'),
        path('delete', views.customer_delete, name='customer_delete'),

    ])),

    path('type/form', views.type_form, name='type_form'),
    path('type/insert', views.type_insert, name='type_insert'),
    path('index', views.type_index, name='type_index'),
    path('<int:type_pk>/', include([
        path('', views.type_read, name='type_read'),
        path('edit', views.type_edit, name='type_edit'),
        path('delete', views.type_delete, name='type_delete'),

    ])),
]