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
from rest_framework import routers
from api.v2.customer import viewsets
from api.v2.request import viewsets as requestViewSets
from api.v2.account import viewsets as accountViewSets
from api.v2.motorCodes import viewSets as motorCodeViewSets

router = routers.SimpleRouter()
router.register('users', accountViewSets.UserViewSets)
router.register('requests', requestViewSets.RequestViewSets)
router.register('reqspecs', requestViewSets.ReqSpecViewSets)
router.register('imtypes', requestViewSets.ImTypeViewSets)
router.register('ictypes', requestViewSets.IcTypeViewSets)
router.register('iptypes', requestViewSets.IpTypeViewSets)
router.register('ietypes', requestViewSets.IeTypeViewSets)
router.register('motorCodes', motorCodeViewSets.MotorCodesViewSets)
router.register('proformas', requestViewSets.XprefViewSets)
router.register('prefspecs', requestViewSets.PrefSpecViewSets)
router.register('incomes', requestViewSets.IncomeViewSets)
router.register('customers', viewsets.CustomerViewSet)
router.register('addresses', viewsets.AddressViewSet)
router.register('phones', viewsets.PhoneViewSet)
app_name = 'apivs'
urlpatterns = [
                  path('v1/', include('api.v1.url')),
                  path('v2/', include(router.urls)),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
