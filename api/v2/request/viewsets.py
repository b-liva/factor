from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from api.permissions.permissions import IsSuperUserOrOwner
from customer.models import Customer
from request.models import Requests, ReqSpec, Xpref, PrefSpec, Payment, IMType, ICType, IPType, IEType
from api.serializers import requestSerializers
from api.permissions import permissions as ApiPermisssions
import jdatetime, datetime

class RequestViewSets(viewsets.ModelViewSet):
    permission_classes = (
        IsSuperUserOrOwner,
        # permissions.DjangoModelPermissions,
    )
    queryset = Requests.objects.filter(is_active=True)
    lookup_field = 'number'
    serializer_class = requestSerializers.RequestSerializers

    # def get_queryset(self):
    #     queryset = self.get_queryset()
    #     return queryset

    def date_correction(self, date):
        """
        corrects the persian date registrations due to djanggo_jalali incompatibility with DRF
        :param date:
        :return: date
        """
        date = date.replace('/', '-')
        return jdatetime.datetime.strptime(date, "%Y-%m-%d").date().togregorian()

    def create(self, request, *args, **kwargs):
        request.data['owner'] = request.user.pk
        request.data['date_fa'] = self.date_correction(request.data['date_fa'])
        return super(RequestViewSets, self).create(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def reqspecs(self, request, pk=None, **kwargs):
        reqspecs = ReqSpec.objects.filter(
            req_id__number=kwargs['number']
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
    permission_classes = (IsSuperUserOrOwner,)
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
    permission_classes = (IsSuperUserOrOwner,)
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
