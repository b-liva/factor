from rest_framework import serializers
from motordb.models import MotorsCode


class MotorCodesSerializers(serializers.ModelSerializer):

    class Meta:
        model = MotorsCode
        fields = "__all__"

