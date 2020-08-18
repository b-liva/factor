from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
User = get_user_model()
from api.serializers import accountSerializers


class UserViewSets(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = User.objects.all()
    serializer_class = accountSerializers.UserSerializers

