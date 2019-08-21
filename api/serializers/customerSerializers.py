import jdatetime
from rest_framework import serializers
from customer.models import Customer, Address, Phone
from api.serializers.requestSerializers import DateCorrection


class PhoneSerializers(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = "__all__"


class AddressSerializers(serializers.ModelSerializer):
    phone_set = PhoneSerializers(many=True, read_only=True)

    class Meta:
        model = Address
        fields = "__all__"


class CustomerSerializer(DateCorrection, serializers.ModelSerializer):
    address_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    requests_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Customer
        # fields = ('pk', 'name', 'owner', 'type')
        fields = "__all__"
        read_only_fields = ['owner', 'date', 'date2']

    def create(self, validated_data):

        if 'date2' in self.validated_data:
            validated_data['date2'] = self.date_correction(str(self.validated_data.get('date2')))
        else:
            validated_data['date2'] = jdatetime.datetime.now().date()

        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
