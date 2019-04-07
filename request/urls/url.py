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

urlpatterns = [
                  path('project_type', request.views2.project_type_form, name='project_type_form'),
                  path('project-type/index', request.views2.projects_type_index, name='projects_type_index'),

                  path('img/<int:img_pk>/del', request.views2.image_delete, name='image_delete'),
                  path('<int:img_pk>/img/del', request.views2.img_del, name='img_del'),
                  path('<int:img_pk>/prof_img/del', request.views2.prof_img_del, name='prof_img_del'),

                  path('', include('request.urls.req_urls')),
                  path('pref/', include('request.urls.prof_urls')),
                  path('payment/', include('request.urls.payment_urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
