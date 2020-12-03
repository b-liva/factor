from rest_framework import (generics, permissions)
from django_filters.rest_framework import DjangoFilterBackend

from cost.filters.filters import WageCostFilter
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
    filter_backends = [DjangoFilterBackend]
    # filter_fields = ('qty', 'price')
    filterset_class = WageCostFilter

    def get_queryset(self):
        # print("request: ", self.request.query_params)
        return WageCost.objects.filter(owner=self.request.user)


class WageCostManager(generics.RetrieveUpdateDestroyAPIView):
    queryset = WageCost.objects.all()
    serializer_class = WageCostSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        CustomDjangoModelPermissions,
        CustomDjangoObjectPermissions
    ]
