from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import request.views
# from z_mine.request.routers import router
from request.viewsFolder import perm_views
app_name = 'perms'
urlpatterns = [
                  path('form', perm_views.form, name='pro_form'),
                  path('index', perm_views.perm_index, name='perm_index'),
                  path('find', perm_views.perm_find, name='perm_find'),
                  path('<int:perm_pk>/', include([
                      path('', perm_views.perm_details, name='perm_details'),
                      path('delete', perm_views.perm_delete, name='perm_delete'),
                      path('edit', perm_views.perm_edit, name='perm_edit'),
                  ])),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
