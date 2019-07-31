from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CustomerSerializer
from customer.models import Customer


class ListCustomers(APIView):
    def get(self, request, format=None):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
