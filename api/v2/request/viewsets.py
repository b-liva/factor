from rest_framework import viewsets
from request.models import Requests, ReqSpec, Xpref, PrefSpec, Payment
from api.serializers import requestSerializers


class RequestViewSets(viewsets.ModelViewSet):
    queryset = Requests.objects.filter(is_active=True)
    serializer_class = requestSerializers.RequestSerializers


class ReqSpecViewSets(viewsets.ModelViewSet):
    queryset = ReqSpec.objects.filter(is_active=True)
    serializer_class = requestSerializers.ReqSpecSerializers


class XprefViewSets(viewsets.ModelViewSet):
    queryset = Xpref.objects.filter(is_active=True)
    serializer_class = requestSerializers.XprefSerializers


class PrefSpecViewSets(viewsets.ModelViewSet):
    queryset = PrefSpec.objects.all()
    serializer_class = requestSerializers.PrefSpecSerializers


class IncomeViewSets(viewsets.ModelViewSet):
    queryset = Payment.objects.filter(is_active=True)
    serializer_class = requestSerializers.IncomeSerializers
