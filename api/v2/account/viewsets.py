from rest_framework import viewsets, permissions
from accounts.models import User, CustomerUser
from api.serializers import accountSerializers


class UserViewSets(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = User.objects.all()
    serializer_class = accountSerializers.UserSerializers


class CustomerUserViewSets(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = CustomerUser.objects.all()
    serializer_class = accountSerializers.CustomerUserSerializers
