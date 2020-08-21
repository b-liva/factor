from rest_framework import viewsets
from ..models import Xpref, Payment
from z_mine.request.serializers import PaymentSerializer, XprefSerializer


class XprefViewSet(viewsets.ModelViewSet):
    queryset = Xpref.objects.all()[:100]
    serializer_class = XprefSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()[:100]
    serializer_class = PaymentSerializer

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['foo'] = 'bar'
    #     return context

    # def get_renderer_context(self):
    #     context = super().get_renderer_context()
    #     context['foo'] = 'bar'
    #     return context



