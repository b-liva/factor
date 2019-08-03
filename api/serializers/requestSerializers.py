from rest_framework import serializers
from request.models import Requests, ReqSpec, Xpref, PrefSpec, Payment


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
