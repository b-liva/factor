from rest_framework import generics

from .serializers import CustomerSerializer
from customer.models import Customer


class ListCreateCustomer(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class RetrieveUpdateDestroyCustomer(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
