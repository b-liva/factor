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

    def get_queryset(self):
        return WageCost.objects.filter(owner=self.request.user)


class WageCostManager(generics.RetrieveUpdateDestroyAPIView):
    queryset = WageCost.objects.all()
    serializer_class = WageCostSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        CustomDjangoModelPermissions,
        CustomDjangoObjectPermissions
    ]
