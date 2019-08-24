from rest_framework import serializers
from motordb.models import MotorsCode


class MotorCodesSerializers(serializers.ModelSerializer):

    class Meta:
        model = MotorsCode
        fields = "__all__"

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
