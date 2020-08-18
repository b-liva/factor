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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views
urlpatterns = [
    path('add', views.speccm_add, name='speccm_add'),
    path('add-vue', views.speccm_vueadd, name='speccm_add_vue'),
    path('index', views.speccm_index, name='speccm_index'),
    path('get_chat', views.get_chat, name='get_chat'),
    path('<int:speccm_pk>/', include([
        path('', views.speccm_read, name='speccm_read'),
        path('del', views.speccm_delete, name='speccm_del'),
    ])),
    path('report', views.speccm_report, name='speccm_report'),
]

