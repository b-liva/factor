from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from request.models import Requests, ReqSpec, Xpref, PrefSpec, Payment, IMType, ICType, IPType, IEType
from api.serializers import requestSerializers
from api.permissions import permissions as CustomPerms
import datetime
import jdatetime


class RequestViewSets(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticated,
        CustomPerms.IsSuperUserOrOwner,
        CustomPerms.CustomDjangoModelPermission,
        # permissions.DjangoModelPermissions,
    )
    queryset = Requests.objects.filter(is_active=True)
    deleted_queryset = Requests.objects.filter(is_active=False)
    lookup_field = 'number'
    serializer_class = requestSerializers.RequestSerializers

    def get_queryset(self):
        if self.request.user.is_superuser:
            # todo: everywhere should updated with actives or is_active=True
            # todo: In the next version deletion should be cascaded but a copy of the object should be created
            # todo: some permission defenition required. such as list all. update all, delete all, etc.
            return self.queryset
        return self.queryset.filter(owner=self.request.user)

    def date_correction(self, date):
        """
        corrects the persian date registrations due to djanggo_jalali incompatibility with DRF
        :param date:
        :return: date
        """
        date = date.replace('/', '-')
        return jdatetime.datetime.strptime(date, "%Y-%m-%d").date().togregorian()

    @action(detail=True, methods=['get'])
    def reqspecs(self, request, pk=None, **kwargs):
        reqspecs = ReqSpec.objects.filter(
            req_id__number=kwargs['number']
        )
        serializer = requestSerializers.ReqSpecSerializers(reqspecs, many=True)
        return Response(serializer.data)


class ReqSpecViewSets(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticated,
        CustomPerms.IsSuperUserOrOwner,
        # CustomPerms.CustomDjangoModelPermission,
        permissions.DjangoModelPermissions,
    )
    queryset = ReqSpec.objects.filter(is_active=True)
    serializer_class = requestSerializers.ReqSpecSerializers


class XprefViewSets(viewsets.ModelViewSet):
    permission_classes = (CustomPerms.IsSuperUserOrOwner,)
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
    permission_classes = (CustomPerms.IsSuperUserOrOwner,)
    queryset = Payment.objects.filter(is_active=True)
    serializer_class = requestSerializers.IncomeSerializers


class ImTypeViewSets(viewsets.ModelViewSet):
    queryset = IMType.objects.all()
    serializer_class = requestSerializers.ImTypeSerializers


class IcTypeViewSets(viewsets.ModelViewSet):
    queryset = ICType.objects.all()
    serializer_class = requestSerializers.IcTypeSerializers


class IpTypeViewSets(viewsets.ModelViewSet):
    queryset = IPType.objects.all()
    serializer_class = requestSerializers.IpTypeSerializers


class IeTypeViewSets(viewsets.ModelViewSet):
    queryset = IEType.objects.all()
    serializer_class = requestSerializers.IeTypeSerializers
