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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import prefactor.views
import prefactor_verification.views
import tender.views
import request.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', prefactor.views.home, name='homepage'),
    path('prefPage/', prefactor.views.prefactors, name='prefPage'),
    path('pref_ver/', prefactor_verification.views.pref_verification, name='pref_ver'),
    path('tenders/', tender.views.tenders, name='tenders'),
    path('requests/', request.views.request_page, name="requestPage"),
    path('prefactors/', request.views.prefactors_page, name="prefactorsPage"),
    path('prefVerification/', request.views.prefactors_verification_page, name="prefVerificationPage")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
