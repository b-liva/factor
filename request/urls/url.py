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

import request.views
from request import views2
from request import reqSpecViews
from request.viewsFolder import permission


urlpatterns = [


path('request/', request.views.createpage, name='createpage'),

    path('project_type', request.views2.project_type_form, name='project_type_form'),
    path('project-type/index', request.views2.projects_type_index, name='projects_type_index'),

    path('pref_spec/add', request.views2.pref_spec_add, name='pref_spec_add'),
    path('pref_spec/<int:ypref_spec_pk>/', include([
        path('', request.views2.pref_spec_details, name='prefspec_details'),
        path('delete', request.views2.pref_spec_del, name='pref_spec_delete'),
        path('edit', request.views2.pref_spec_edit, name='pref_spec_edit'),
    ])),

    path('permission/form', permission.permission_form, name='permission_form'),
    path('permission/insert', permission.permission_insert, name='permission_insert'),
    path('permission/index', permission.permission_index, name='permission_index'),
    path('permission/find', permission.permission_find, name='permission_find'),
    path('permission/<int:permission_pk>/', include([
        path('', permission.permission_details, name='permission_details'),
        path('delete', permission.permission_delete, name='permission_delete'),
        path('edit', permission.permission_edit, name='permission_edit'),
    ])),

    # path('pref/<int:xpref_pk>/forminsert', proformaViews.reqspec_form, name='reqSpec_form'),
    path('<int:req_pk>/reqSpec/<int:yreqSpec_pk>/', include([
        path('', request.reqSpecViews.reqspec_details, name='reqSpec_details'),
    ])),

    path('img/<int:img_pk>/del', request.views2.image_delete, name='image_delete'),
    path('<int:img_pk>/img/del', request.views2.img_del, name='img_del'),
    path('<int:img_pk>/prof_img/del', request.views2.prof_img_del, name='prof_img_del'),

    path('', include('request.urls.req_urls')),
    path('pref/', include('request.urls.prof_urls')),
    path('payment/', include('request.urls.payment_urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
