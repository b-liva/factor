from rest_framework import serializers
from cost.models import ProjectCost


class ProjectCostSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectCost
        fields = "__all__"
