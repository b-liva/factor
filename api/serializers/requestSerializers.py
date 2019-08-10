from rest_framework import serializers
from request.models import Requests, ReqSpec, Xpref, PrefSpec, Payment, IMType, ICType, IPType, IEType


class RequestSerializers(serializers.ModelSerializer):
    reqspec_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Requests
        fields = "__all__"


class ReqSpecSerializers(serializers.ModelSerializer):
    class Meta:
        model = ReqSpec
        fields = "__all__"


class XprefSerializers(serializers.ModelSerializer):
    prefspec_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Xpref
        fields = "__all__"


class PrefSpecSerializers(serializers.ModelSerializer):
    class Meta:
        model = PrefSpec
        fields = "__all__"


class IncomeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class ImTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = IMType
        fields = "__all__"


class IcTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = ICType
        fields = "__all__"


class IpTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = IPType
        fields = "__all__"


class IeTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = IEType
        fields = "__all__"
