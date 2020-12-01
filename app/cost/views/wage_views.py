from rest_framework import (generics, permissions)
from cost.serializers import WageCostSerializer
from cost.permissions import (CustomDjangoModelPermissions, CustomDjangoObjectPermissions)
from cost.models import WageCost


class WageCreateList(generics.ListCreateAPIView):
    queryset = WageCost.objects.all()
    serializer_class = WageCostSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        CustomDjangoModelPermissions,
        CustomDjangoObjectPermissions
    ]


class WageCostManager(generics.RetrieveUpdateDestroyAPIView):
    queryset = WageCost.objects.all()
    serializer_class = WageCostSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        CustomDjangoModelPermissions,
        CustomDjangoObjectPermissions
    ]
