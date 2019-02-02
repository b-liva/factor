from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from request.viewsFolder import paymentViews

urlpatterns = [

    path('testimage', paymentViews.testimage, name='testimage'),
    path('form', paymentViews.payment_form, name='payment_form'),
    path('pay_form', paymentViews.pay_form, name='pay_form'),
    # path('insert', paymentViews.payment_insert, name='payment_insert'),
    path('index', paymentViews.payment_index, name='payment_index'),
    path('index-deleted', paymentViews.payment_index_deleted, name='payment_index_deleted'),
    path('find', paymentViews.payment_find, name='payment_find'),
    path('<int:ypayment_pk>/', include([
      path('', paymentViews.payment_details, name='payment_details'),
      path('delete', paymentViews.payment_delete, name='payment_delete'),
      path('edit', paymentViews.payment_edit, name='payment_edit'),
    ])),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
