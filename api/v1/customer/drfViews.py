from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import CustomerSerializer
from customer.models import Customer


class ListCreateCustomer(APIView):
    def get(self, request, format=None):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CustomerSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
