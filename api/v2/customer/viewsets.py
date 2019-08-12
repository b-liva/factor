from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from api.serializers.customerSerializers import CustomerSerializer, AddressSerializers, PhoneSerializers
from api.permissions.permissions import IsSuperUserOrOwner
from customer.models import Customer, Address, Phone


class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrOwner, permissions.DjangoModelPermissions,)
    queryset = Customer.objects.order_by('name')
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # @detail_route(methods=['get'])
    @action(detail=True, methods=['get'])
    def addresses(self, request, pk=None):
        self.pagination_class.page_size = 2
        # customer = self.get_object()
        # addresses = customer.address_set.all()
        addresses = Address.objects.filter(customer_id=pk)

        page = self.paginate_queryset(addresses)

        if page is not None:
            serializer = AddressSerializers(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = AddressSerializers(addresses, many=True)
        return Response(serializer.data)


class AddressViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Address.objects.all()
    serializer_class = AddressSerializers


class PhoneViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializers
