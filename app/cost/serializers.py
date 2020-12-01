from rest_framework import serializers
from cost.models import (ProjectCost, WageCost,)


class ProjectCostSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectCost
        fields = "__all__"


class WageCostSerializer(serializers.ModelSerializer):

    class Meta:
        model = WageCost
        fields = "__all__"
