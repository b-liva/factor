from rest_framework import serializers
from accounts.models import User, CustomerUser


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class CustomerUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = "__all__"
