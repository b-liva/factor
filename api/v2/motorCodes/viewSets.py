from api.serializers import motorCodesSerializers
from rest_framework import viewsets, permissions
from motordb.models import MotorsCode
from api.permissions import permissions as CustomPerms


class MotorCodesViewSets(viewsets.ModelViewSet):
    queryset = MotorsCode.objects.all()
    serializer_class = motorCodesSerializers.MotorCodesSerializers
    permission_classes = (
        permissions.IsAuthenticated,
        CustomPerms.IsSuperUserOrOwner,
        CustomPerms.CustomDjangoModelPermission,
    )
