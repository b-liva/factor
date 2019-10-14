from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import request.views
# from z_mine.request.routers import router
from request.viewsFolder import invoice_views
app_name = 'invoice'
urlpatterns = [
                  path('form', invoice_views.form, name='pro_form'),
                  path('index', invoice_views.invoice_index, name='invoice_index'),
                  path('find', invoice_views.invoice_find, name='invoice_find'),
                  path('<int:invoice_pk>/', include([
                      path('', invoice_views.invoice_details, name='invoice_details'),
                      path('delete', invoice_views.invoice_delete, name='invoice_delete'),
                      path('edit', invoice_views.invoice_edit, name='invoice_edit'),
                  ])),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
