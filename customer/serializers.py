from rest_framework import serializers
from rest_framework.utils import json

from .models import Customer
from request.serializers import PaymentSerializer


class CustomerSerializer(serializers.ModelSerializer):
    # payments = PaymentSerializer()

    class Meta:
        model = Customer
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Access self.context here to add contextual data into ret
        ret['new_name'] = instance.name
        ret['total_receivable'] = instance.total_receivable()
        ret['total_received'] = json.dumps(instance.total_received()['payments'])
        print('ret', ret['total_received'])
        return ret
