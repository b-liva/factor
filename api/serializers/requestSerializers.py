import jdatetime
from rest_framework import serializers
from request.models import Requests, ReqSpec, Xpref, PrefSpec, Payment, IMType, ICType, IPType, IEType


class DateCorrection:

    def date_correction(self, date):
        """
        corrects the persian date registrations due to djanggo_jalali incompatibility with DRF
        :param date:
        :return: date
        """
        date = date.replace('/', '-')
        return jdatetime.datetime.strptime(date, "%Y-%m-%d").date().togregorian()


class RequestSerializers(DateCorrection, serializers.ModelSerializer):
    reqspec_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Requests
        fields = "__all__"
        read_only_fields = ['owner']

    def create(self, validated_data):

        if 'date_fa' in self.validated_data:
            validated_data['date_fa'] = self.date_correction(str(self.validated_data.get('date_fa')))
        else:
            validated_data['date_fa'] = jdatetime.datetime.now().date()

        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class ReqSpecSerializers(serializers.ModelSerializer):
    class Meta:
        model = ReqSpec
        fields = "__all__"


class XprefSerializers(DateCorrection, serializers.ModelSerializer):
    prefspec_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Xpref
        fields = "__all__"
        # read_only_fields = ['date_fa', 'pub_date', 'date_modified', 'exp_date_fa']

    def create(self, validated_data):
        if 'date_fa' in self.validated_data:
            validated_data['date_fa'] = self.date_correction(str(self.validated_data.get('date_fa')))
        else:
            validated_data['date_fa'] = jdatetime.datetime.now().date()
        if 'exp_date_fa' in self.validated_data:
            validated_data['exp_date_fa'] = self.date_correction(str(self.validated_data.get('exp_date_fa')))
        else:
            validated_data['exp_date_fa'] = jdatetime.datetime.now().date()
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class PrefSpecSerializers(serializers.ModelSerializer):
    class Meta:
        model = PrefSpec
        fields = "__all__"
        read_only_fields = ['kw', 'rpm']

    def create(self, validated_data):
        # todo: needs more work...
        reqspec = validated_data.get('reqspec_eq')
        validated_data['kw'] = reqspec.kw
        validated_data['rpm'] = reqspec.rpm
        return super().create(validated_data)


class IncomeSerializers(DateCorrection, serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

    def create(self, validated_data):

        if 'date_fa' in self.validated_data:
            validated_data['date_fa'] = self.date_correction(str(self.validated_data.get('date_fa')))
        else:
            validated_data['date_fa'] = jdatetime.datetime.now().date()

        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


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
