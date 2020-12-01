from rest_framework import (generics, permissions)
from cost.serializers import ProjectCostSerializer
from cost.permissions import (CustomDjangoModelPermissions, CustomDjangoObjectPermissions)
from cost.models import ProjectCost


# Create your views here.
class ProjectCostList(generics.ListCreateAPIView):
    queryset = ProjectCost.objects.all()
    serializer_class = ProjectCostSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        CustomDjangoModelPermissions,
        CustomDjangoObjectPermissions
    ]


class ProjectCostManage(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectCost.objects.all()
    serializer_class = ProjectCostSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        CustomDjangoModelPermissions,
        CustomDjangoObjectPermissions
    ]
