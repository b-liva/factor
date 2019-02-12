from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
    UpdateAPIView,
    CreateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from fund.api.serializers import (
    FundListSerializer,
    FundDetailsSerializer,
    FundCreateSerializer,
)
from fund.models import Fund
from fund.api.permissions import HasPermOrIsOwner

class FundCreateAPIView(CreateAPIView):
    queryset = Fund.objects.all()
    serializer_class = FundCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        # serializer.save(owner=self.request.user, title='a fix title')


class FundListAPIView(ListAPIView):
    queryset = Fund.objects.all()
    serializer_class = FundListSerializer


class FundDetailAPIView(RetrieveAPIView):
    queryset = Fund.objects.all()
    serializer_class = FundDetailsSerializer


# class FundUpdateApiView(UpdateAPIView):
class FundUpdateApiView(RetrieveUpdateAPIView):
    queryset = Fund.objects.all()
    serializer_class = FundDetailsSerializer
    permission_classes = [IsAuthenticated, HasPermOrIsOwner]

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)
        # serializer.save(owner=self.request.user, title='a fix title')


class FundDeleteApiView(DestroyAPIView):
    queryset = Fund.objects.all()
    serializer_class = FundDetailsSerializer
