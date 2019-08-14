import jdatetime
from rest_framework import serializers
from request.models import Requests, ReqSpec, Xpref, PrefSpec, Payment, IMType, ICType, IPType, IEType


class RequestSerializers(serializers.ModelSerializer):
    reqspec_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def date_correction(self, date):
        """
        corrects the persian date registrations due to djanggo_jalali incompatibility with DRF
        :param date:
        :return: date
        """
        date = date.replace('/', '-')
        return jdatetime.datetime.strptime(date, "%Y-%m-%d").date().togregorian()

    class Meta:
        model = Requests
        fields = "__all__"

    def create(self, validated_data):
        validated_data['date_fa'] = self.date_correction(str(self.validated_data.get('date_fa')))
        validated_data['owner'] = self.context['request'].user
        return super(RequestSerializers, self).create(validated_data)


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
