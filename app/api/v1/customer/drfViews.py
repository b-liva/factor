from django.shortcuts import get_object_or_404
from rest_framework import generics

from api.serializers.customerSerializers import CustomerSerializer, AddressSerializers
from customer.models import Customer, Address


class ListCreateCustomer(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class RetrieveUpdateDestroyCustomer(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_url_kwarg = 'customer_pk'


class ListCreateAddress(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializers

    def get_queryset(self):
        return self.queryset.filter(customer=self.kwargs.get('customer_pk'))

    def perform_create(self, serializer):
        customer = get_object_or_404(Customer, pk=self.kwargs['customer_pk'])
        serializer.save(customer=customer)


class RetrieveUpdateDestroyAddress(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializers
    lookup_url_kwarg = 'address_pk'

    def get_object(self):
        obj = get_object_or_404(
            self.queryset,
            customer=self.kwargs.get('customer_pk'),
            pk=self.kwargs.get('address_pk')
        )
        return obj
