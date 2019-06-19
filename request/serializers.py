from rest_framework import serializers
from .models import Requests, Xpref, Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class XprefSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer()
    # payments = serializers.StringRelatedField(many=True)

    class Meta:
        model = Xpref
        fields = '__all__'

