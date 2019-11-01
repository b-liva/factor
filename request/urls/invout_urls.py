from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import request.views
# from z_mine.request.routers import router
from request.viewsFolder import invout_views
app_name = 'invout'
urlpatterns = [
                  path('form', invout_views.form, name='pro_form'),
                  path('index', invout_views.invout_index, name='invout_index'),
                  path('find', invout_views.invout_find, name='invout_find'),
                  path('<int:invout_pk>/', include([
                      path('', invout_views.invout_details, name='invout_details'),
                      path('delete', invout_views.invout_delete, name='invout_delete'),
                      path('edit', invout_views.invout_edit, name='invout_edit'),
                  ])),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
