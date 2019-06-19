from rest_framework import routers
from .viewsFolder.viewsets import CustomerViewSet

router = routers.DefaultRouter()

router.register('customer', CustomerViewSet)
