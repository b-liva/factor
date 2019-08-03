from rest_framework import serializers
from customer.models import Customer, Address, Phone


class PhoneSerializers(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = "__all__"


class AddressSerializers(serializers.ModelSerializer):
    phone_set = PhoneSerializers(many=True, read_only=True)

    class Meta:
        model = Address
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    address_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    requests_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Customer
        # fields = ('pk', 'name', 'owner', 'type')
        fields = "__all__"
