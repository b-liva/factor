from django.urls import path, include
from cost.views.views import (ProjectCostList, ProjectCostManage, )
from cost.views import wage_views

app_name = 'cost'

urlpatterns = [
    path('create/', ProjectCostList.as_view(), name='create'),
    path('manage/<int:pk>/', ProjectCostManage.as_view(), name='manage'),
    path('manage/<int:pk>/', ProjectCostManage.as_view(), name='manage'),
    path('wage/create/', wage_views.WageCreateList.as_view(), name='create_wage'),
    path('wage/manage/<int:pk>', wage_views.WageCostManager.as_view(), name='manage_wage'),
]
