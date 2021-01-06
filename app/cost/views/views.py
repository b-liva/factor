from rest_framework import (generics, permissions)
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from cost.serializers import ProjectCostSerializer
from cost.permissions import (CustomDjangoModelPermissions, CustomDjangoObjectPermissions)
from cost.models import ProjectCost


class CustomPagination(PageNumberPagination):
    page_size = 5


# Create your views here.
class ProjectCostList(generics.ListCreateAPIView):
    queryset = ProjectCost.objects.all()
    serializer_class = ProjectCostSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        CustomDjangoModelPermissions,
        CustomDjangoObjectPermissions
    ]
    pagination_class = CustomPagination

    def get_queryset(self):
        return ProjectCost.objects.filter(owner=self.request.user)


class ProjectCostManage(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectCost.objects.all()
    serializer_class = ProjectCostSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        CustomDjangoModelPermissions,
        CustomDjangoObjectPermissions
    ]
