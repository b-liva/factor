from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.customer, name='customer'),
    path('create', views.customer_create, name='customer_create'),
    path('view', views.customer_read, name='customer_view'),
    path('update', views.customer_update, name='customer_update'),
    path('delete', views.customer_delete, name='customer_delete'),
    path('customer_type/create', views.type_create, name='customer_type_create'),
    path('customer_type/view', views.type_read, name='customer_type_view'),
    path('customer_type/update', views.type_update, name='customer_type_update'),
    path('customer_type/delete', views.type_delete, name='customer_type_delete'),
    path('testview', views.TestView.as_view(), name='testview'),
]