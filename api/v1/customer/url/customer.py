"""factor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from api.v1.customer.views import customer_views
from api.v1.customer.classbased import classbased
from api.v1.customer import drfViews

app_name = 'customer'
urlpatterns = [
                  path('index/', customer_views.customer_index, name='customer_index'),
                  path('home/', classbased.Homeview.as_view(), name='home'),
                  path('list/', classbased.CustomerListView.as_view(), name='list'),
                  path('details/<int:pk>', classbased.CustomerDetailsView.as_view(), name='details'),
                  path('create/', classbased.CustomerCreateView.as_view(), name='create'),
                  path('update/<int:pk>', classbased.CustomerUpdateView.as_view(), name='update'),
                  path('hello/', classbased.HelloWorldVie.as_view(), name='hello'),

                  path('list-create-customer/', drfViews.ListCreateCustomer.as_view(), name='list-create-customer'),
                  path('rud-customer/<int:pk>', drfViews.RetrieveUpdateDestroyCustomer.as_view(), name='rud-customer'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
