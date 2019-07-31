from rest_framework import serializers
from customer.models import Customer, Address, Phone


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        # fields = ('pk', 'name', 'owner', 'type')
        fields = "__all__"


class AddressSerializers(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = "__all__"


class PhoneSerializers(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = "__all__"

