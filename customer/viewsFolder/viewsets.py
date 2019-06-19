from rest_framework import viewsets
from ..models import Customer
from ..serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()[:100]
    serializer_class = CustomerSerializer

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     print('context', context)
    #     context['foo'] = 'bar'
    #     return context

    # def get_renderer_context(self):
    #     context = super().get_renderer_context()
    #     context['foo'] = 'bar'
    #     return context



