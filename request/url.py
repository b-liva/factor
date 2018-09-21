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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import prefactor.views
import prefactor_verification.views
import tender.views
import request.views

urlpatterns = [
    path('createpage/', request.views.createpage, name='createpage'),
    path('create_req/', request.views.create_req, name='create_req'),
    path('createprefpage/', request.views.createprefpage, name='createprefpage'),
    path('create_pref/', request.views.create_pref, name='create_pref'),
    path('create_verf_page/', request.views.create_verf_page, name='create_verf_page'),
    path('create_verf/', request.views.create_verf, name='create_verf')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

