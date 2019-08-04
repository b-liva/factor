from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from api.permissions.permissions import IsSuperUserOrOwner
from request.models import Requests, ReqSpec, Xpref, PrefSpec, Payment
from api.serializers import requestSerializers
from api.permissions import permissions as ApiPermisssions


class RequestViewSets(viewsets.ModelViewSet):
    permission_classes = (
        IsSuperUserOrOwner,
        # permissions.DjangoModelPermissions,
    )
    queryset = Requests.objects.filter(is_active=True)
    serializer_class = requestSerializers.RequestSerializers

    # def get_queryset(self):
    #     queryset = self.get_queryset()
    #     return queryset

    @action(detail=True, methods=['get'])
    def reqspecs(self, request, pk=None):
        reqspecs = ReqSpec.objects.filter(
            req_id_id=pk
        )
        serializer = requestSerializers.ReqSpecSerializers(reqspecs, many=True)
        return Response(serializer.data)


class ReqSpecViewSets(viewsets.ModelViewSet):
    permission_classes = (
        ApiPermisssions.IsSuperUserOrOwner,
        permissions.DjangoModelPermissions,
    )
    queryset = ReqSpec.objects.filter(is_active=True)
    serializer_class = requestSerializers.ReqSpecSerializers


class XprefViewSets(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Xpref.objects.filter(is_active=True)
    serializer_class = requestSerializers.XprefSerializers

    @action(detail=True, methods=['get'])
    def prefspecs(self, request, pk=None):
        prefspecs = PrefSpec.objects.filter(xpref_id_id=pk)
        serializer = requestSerializers.PrefSpecSerializers(prefspecs, many=True)
        return Response(serializer.data)


class PrefSpecViewSets(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = PrefSpec.objects.all()
    serializer_class = requestSerializers.PrefSpecSerializers


class IncomeViewSets(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Payment.objects.filter(is_active=True)
    serializer_class = requestSerializers.IncomeSerializers
