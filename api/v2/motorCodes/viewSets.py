from api.serializers import motorCodesSerializers
from rest_framework import viewsets
from motordb.models import MotorsCode


class MotorCodesViewSets(viewsets.ModelViewSet):
    queryset = MotorsCode.objects.all()
    serializer_class = motorCodesSerializers.MotorCodesSerializers
