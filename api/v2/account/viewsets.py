from rest_framework import viewsets
from accounts.models import User, CustomerUser
from api.serializers import accountSerializers


class UserViewSets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = accountSerializers.UserSerializers


class CustomerUserViewSets(viewsets.ModelViewSet):
    queryset = CustomerUser.objects.all()
    serializer_class = accountSerializers.CustomerUserSerializers
