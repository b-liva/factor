from rest_framework import routers
from .viewsFolder.viewsets import PaymentViewSet, XprefViewSet

router = routers.DefaultRouter()

router.register('payment', PaymentViewSet)
router.register('xpref', XprefViewSet)
