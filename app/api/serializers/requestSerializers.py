import jdatetime
from rest_framework import serializers

from motordb.models import MotorsCode
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
        read_only_fields = ['owner']

    def create(self, validated_data):

        if 'im' in validated_data and 'ip' in validated_data and 'ic' in validated_data:
            code = MotorsCode.objects.get(
                kw=validated_data['kw'],
                speed=validated_data.get('rpm_new').rpm,
                voltage=validated_data['voltage'],
                im=validated_data['im'],
                ip=validated_data['ip'],
                ic=validated_data['ic'],
            )
            codes = MotorsCode.objects.all().first()
            # print('********code: ', codes.kw, codes.speed, codes.voltage, codes.im, codes.ip, codes.ic, codes.ie)
            # print('********spec: ', validated_data['kw'], validated_data['rpm_new'], validated_data['voltage'], validated_data['im'], validated_data['ip'], validated_data['ic'], validated_data['ie'])
            validated_data['code'] = code.code
        else:
            validated_data['code'] = 99009900
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


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
