from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from request.models import Requests, ReqSpec, Xpref, PrefSpec, Payment
from api.serializers import requestSerializers


class RequestViewSets(viewsets.ModelViewSet):
    queryset = Requests.objects.filter(is_active=True)
    serializer_class = requestSerializers.RequestSerializers

    @action(detail=True, methods=['get'])
    def reqspecs(self, request, pk=None):
        reqspecs = ReqSpec.objects.filter(
            req_id_id=pk
        )
        serializer = requestSerializers.ReqSpecSerializers(reqspecs, many=True)
        return Response(serializer.data)


class ReqSpecViewSets(viewsets.ModelViewSet):
    queryset = ReqSpec.objects.filter(is_active=True)
    serializer_class = requestSerializers.ReqSpecSerializers


class XprefViewSets(viewsets.ModelViewSet):
    queryset = Xpref.objects.filter(is_active=True)
    serializer_class = requestSerializers.XprefSerializers

    @action(detail=True, methods=['get'])
    def prefspecs(self, request, pk=None):
        prefspecs = PrefSpec.objects.filter(xpref_id_id=pk)
        serializer = requestSerializers.PrefSpecSerializers(prefspecs, many=True)
        return Response(serializer.data)


class PrefSpecViewSets(viewsets.ModelViewSet):
    queryset = PrefSpec.objects.all()
    serializer_class = requestSerializers.PrefSpecSerializers


class IncomeViewSets(viewsets.ModelViewSet):
    queryset = Payment.objects.filter(is_active=True)
    serializer_class = requestSerializers.IncomeSerializers
