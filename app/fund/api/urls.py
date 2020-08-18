from django.contrib import admin
from django.urls import path

from fund.api.views import (
    FundCreateAPIView,
    FundListAPIView,
    FundDetailAPIView,
    FundDeleteApiView,
    FundUpdateApiView,
)

urlpatterns = [
    path('', FundListAPIView.as_view(), name='index'),
    path('create', FundCreateAPIView.as_view(), name='create'),
    path('<int:pk>/', FundDetailAPIView.as_view(), name='details'),
    path('<int:pk>/update', FundUpdateApiView.as_view(), name='update'),
    path('<int:pk>/delete', FundDeleteApiView.as_view(), name='delete'),
]
