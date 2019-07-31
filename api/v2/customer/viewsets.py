from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action, detail_route
from api.v1.customer.serializers import CustomerSerializer, AddressSerializers
from customer.models import Customer, Address


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    # @detail_route(methods=['get'])
    @action(detail=True, methods=['get'])
    def addresses(self, request, pk=None):
        print('entered addrs')
        customer = self.get_object()
        print(customer)
        addresses = customer.address_set.all()
        print(addresses)
        serializer = AddressSerializers(addresses, many=True)
        return Response(serializer.data)


class AddressViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    
    queryset = Address.objects.all()
    serializer_class = AddressSerializers
