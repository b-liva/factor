from django.urls import path, include
from cost.views import (ProjectCostList, ProjectCostManage)

app_name = 'cost'

urlpatterns = [
    path('create/', ProjectCostList.as_view(), name='create'),
    path('manage/<int:pk>/', ProjectCostManage.as_view(), name='manage'),
]
